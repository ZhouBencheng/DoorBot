import cv2
import face_recognition

current_people = "zbc"


def cv_loop():
    # 加载已知人物的照片并学习如何识别它们
    known_image = face_recognition.load_image_file("./me.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # 创建已知面部编码的列表及其名字
    known_face_encodings = [known_face_encoding]
    known_face_names = ["zbc"]

    # 初始化摄像头
    video_capture = cv2.VideoCapture(0)

    while True:
        # 捕捉一帧视频
        ret, frame = video_capture.read()

        # 查找视频帧中的所有面部及其面部编码
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # 查看面部是否与已知面部匹配
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.5)

            name = "Unknown"

            # 如果在已知面部编码中找到匹配项，则使用第一个匹配项的名字
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            global current_people
            current_people = name
            # 画出面部的边框和名字
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # 显示结果帧
        cv2.imshow('Video', frame)

        # 按下‘q’键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头和关闭窗口
    video_capture.release()
    cv2.destroyAllWindows()