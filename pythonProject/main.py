import cv2
import multiprocessing
import time
from datetime import datetime

# Глобальный флаг для завершения процессов
exit_flag = False

def capture_and_save(rtsp_url, base_output_filename):
    global exit_flag
    while not exit_flag:
        # Генерируем уникальное имя файла с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_output_filename}_{timestamp}.avi"

        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            print(f"Failed to open the RTSP stream for {rtsp_url}. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        # Определяем параметры записи видео
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Устанавливаем кодек и создаем объект VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

        while not exit_flag:
            ret, frame = cap.read()
            if ret:
                # Устанавливаем размер окна
                cv2.namedWindow(f'Camera - {rtsp_url}', cv2.WINDOW_NORMAL)

                # Отображаем кадр
                cv2.imshow(f'Camera - {rtsp_url}', frame)

                # Записываем кадр в файл
                out.write(frame)
            else:
                print(f"Failed to read a frame from the RTSP stream for {rtsp_url}. Retrying...")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit_flag = True
                break

        # Освобождаем ресурсы
        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # Пример использования с уникальными именами файлов
    process1 = multiprocessing.Process(target=capture_and_save, args=('rtsp://username:password@ip/', 'output_camera1'))
    process2 = multiprocessing.Process(target=capture_and_save, args=('rtsp://username:password@ip/', 'output_camera2'))

    # Запуск процессов
    process1.start()
    process2.start()

    # Ожидание завершения процессов
    process1.join()
    process2.join()