import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, Label
from inference_sdk import InferenceHTTPClient

# Inicializando o cliente da API
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="DTEUmRzESZm6eaVCplPI"
)

# Variável para controlar o estado da detecção
detectar_comprimento = False

# Função de reconhecimento de objetos
def detectar_objetos():
    global detectar_comprimento

    # Capturar vídeo da câmera
    cap = cv2.VideoCapture(0)

    # Diminuir a resolução do frame capturado
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Largura
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Altura

    # Definir a escala com base no objeto conhecido
    known_width_cm = 23
    known_width_px = 118
    scale = known_width_cm / known_width_px

    # Definir o fator de correção para a bounding box
    padding_factor = 0.9

    # Listas para armazenar as medidas
    widths = []
    heights = []
    depths = []

    num_frames_stabilization = 5
    frame_count = 0
    stable_frame_count = 0
    stable_threshold = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame da câmera.")
            break

        temp_image_path = "temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)
        result = CLIENT.infer(temp_image_path, model_id="grid-2zfis/1")

        print(result)

        if "predictions" in result and result["predictions"]:
            for prediction in result["predictions"]:
                x_min = int(prediction['x'] - prediction['width'] / 2)
                y_min = int(prediction['y'] - prediction['height'] / 2)
                x_max = int(prediction['x'] + prediction['width'] / 2)
                y_max = int(prediction['y'] + prediction['height'] / 2)

                width_px = x_max - x_min
                height_px = y_max - y_min

                width_px_adjusted = int(width_px * padding_factor)
                height_px_adjusted = int(height_px * padding_factor)
                x_min_adjusted = x_min + (width_px - width_px_adjusted) // 2
                y_min_adjusted = y_min + (height_px - height_px_adjusted) // 2
                x_max_adjusted = x_min_adjusted + width_px_adjusted
                y_max_adjusted = y_min_adjusted + height_px_adjusted

                width_cm = width_px_adjusted * scale
                height_cm = height_px_adjusted * scale

                if not detectar_comprimento:
                    widths.append(width_cm)
                    heights.append(height_cm)
                    cv2.rectangle(frame, (x_min_adjusted, y_min_adjusted), (x_max_adjusted, y_max_adjusted), (0, 255, 0), 2)
                    label = f"{prediction['class']} W:{width_cm:.2f}cm H:{height_cm:.2f}cm"
                    cv2.putText(frame, label, (x_min_adjusted, y_min_adjusted - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow('Câmera ao vivo', frame)

        if result['predictions']:
            frame_count += 1
        if frame_count > num_frames_stabilization:
            stable_frame_count += 1
            if stable_frame_count >= stable_threshold:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not detectar_comprimento:
        if widths and heights:
            avg_width = sum(widths) / len(widths)
            avg_height = sum(heights) / len(heights)
            entry_width.delete(0, ctk.END)
            entry_width.insert(0, f"{avg_width:.2f}")
            entry_height.delete(0, ctk.END)
            entry_height.insert(0, f"{avg_height:.2f}")
            messagebox.showinfo("Medições", "Altura e Largura capturadas. Clique novamente para medir o comprimento.")
            detectar_comprimento = True
        else:
            messagebox.showinfo("Medições", "Nenhuma medida foi registrada.")
    else:
        # Nova detecção para calcular o comprimento
        widths_depth = []
        heights_depth = []
        num_frames_stabilization_depth = 5
        frame_count_depth = 0
        stable_frame_count_depth = 0
        stable_threshold_depth = 1

        # Captura de vídeo para comprimento
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Falha ao capturar frame da câmera.")
                break

            temp_image_path = "temp_frame_depth.jpg"
            cv2.imwrite(temp_image_path, frame)
            result = CLIENT.infer(temp_image_path, model_id="grid-2zfis/1")

            print(result)

            if "predictions" in result and result["predictions"]:
                for prediction in result["predictions"]:
                    x_min = int(prediction['x'] - prediction['width'] / 2)
                    y_min = int(prediction['y'] - prediction['height'] / 2)
                    x_max = int(prediction['x'] + prediction['width'] / 2)
                    y_max = int(prediction['y'] + prediction['height'] / 2)

                    width_px = x_max - x_min
                    height_px = y_max - y_min

                    width_px_adjusted = int(width_px * padding_factor)
                    height_px_adjusted = int(height_px * padding_factor)
                    x_min_adjusted = x_min + (width_px - width_px_adjusted) // 2
                    y_min_adjusted = y_min + (height_px - height_px_adjusted) // 2
                    x_max_adjusted = x_min_adjusted + width_px_adjusted
                    y_max_adjusted = y_min_adjusted + height_px_adjusted

                    width_cm = width_px_adjusted * scale
                    height_cm = height_px_adjusted * scale

                    widths_depth.append(width_cm)
                    heights_depth.append(height_cm)

                    cv2.rectangle(frame, (x_min_adjusted, y_min_adjusted), (x_max_adjusted, y_max_adjusted), (0, 255, 0), 2)
                    label = f"{prediction['class']} W:{width_cm:.2f}cm H:{height_cm:.2f}cm"
                    cv2.putText(frame, label, (x_min_adjusted, y_min_adjusted - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.imshow('Câmera ao vivo', frame)

            if result['predictions']:
                frame_count_depth += 1
            if frame_count_depth > num_frames_stabilization_depth:
                stable_frame_count_depth += 1
                if stable_frame_count_depth >= stable_threshold_depth:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if widths_depth and heights_depth:
            avg_depth = sum(heights_depth) / len(heights_depth)
            entry_depth.delete(0, ctk.END)
            entry_depth.insert(0, f"{avg_depth:.2f}")
            avg_width = float(entry_width.get())
            avg_height = float(entry_height.get())
            weight = (avg_height * avg_width * avg_depth) / 6000
            entry_weight.delete(0, ctk.END)
            entry_weight.insert(0, f"{weight:.2f}")
            messagebox.showinfo("Medições", "Comprimento e Peso calculados com sucesso.")
            detectar_comprimento = False

# Interface gráfica com CustomTkinter
def criar_interface():
    global entry_width, entry_height, entry_depth, entry_weight

    ctk.set_appearance_mode("light")  # Opções: "light", "dark"
    ctk.set_default_color_theme("blue")  # Defina o tema das cores

    root = ctk.CTk()  # Use ctk.CTk() para a janela principal

    # Carregar e configurar a imagem
    image_path = "imgs/logo-correios1.png"  # Substitua pelo caminho para sua imagem
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((100, 68))  # Redimensionar a imagem para 100x68 pixels

    # Converter a imagem para um formato que o tkinter pode usar
    tk_image = ImageTk.PhotoImage(pil_image)

    # Criar um label para exibir a imagem
    image_label = Label(root, image=tk_image)
    image_label.pack(pady=20)

    # Manter a referência da imagem para evitar que ela seja coletada pelo garbage collector
    image_label.image = tk_image

    root.title("Reconhecimento de Objetos")

    # Tamanho da janela
    root.geometry("350x650")

    # Título
    title_label = ctk.CTkLabel(root, text="Medição do Pacote", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Frame para organizar os campos
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Campos de entrada
    ctk.CTkLabel(main_frame, text="Altura (cm):").pack(pady=5)
    entry_height = ctk.CTkEntry(main_frame)
    entry_height.pack(pady=5)

    ctk.CTkLabel(main_frame, text="Largura (cm):").pack(pady=5)
    entry_width = ctk.CTkEntry(main_frame)
    entry_width.pack(pady=5)

    ctk.CTkLabel(main_frame, text="Comprimento (cm):").pack(pady=5)
    entry_depth = ctk.CTkEntry(main_frame)
    entry_depth.pack(pady=5)

    ctk.CTkLabel(main_frame, text="Peso (kg):").pack(pady=5)
    entry_weight = ctk.CTkEntry(main_frame)
    entry_weight.pack(pady=5)

    # Botão para iniciar a detecção
    btn_detectar = ctk.CTkButton(main_frame, text="Iniciar Detecção", command=detectar_objetos)
    btn_detectar.pack(pady=20)

    root.mainloop()

# Executar a interface gráfica
criar_interface()
