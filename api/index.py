import glob
import os
from flask import Flask, request, jsonify
import numpy as np
import cv2 as cv
from flask_cors import CORS
import random
from utils import girl_images


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config['SECRET_KEY'] = 'very_secret'
app.secret_key = 'very_secret'
app.config.from_object(__name__)
# CORS(app)


def get_new_image_path(user_id, file_extension):
    new_user_id_dir = os.path.join('../user_images', f'{user_id}')
    os.makedirs(new_user_id_dir, exist_ok=True)
    dir_list = glob.glob(f'{new_user_id_dir}/*')
    dir_count = len(dir_list)
    new_image_path = os.path.join(new_user_id_dir, f'{dir_count}{file_extension}')
    return new_image_path

#
# from api import db_manager
#
#
# @app.route('/buy-monthly-premium', methods=['GET'])
# def buy_monthly_premium():
#     try:
#         if random.randint(0, 1) == 1:
#             return {'purchase': False}
#
#         client_id = request.args.get('id')
#         db_manager.buy_monthly_premium_with_client_id(client_id=client_id)
#         return {'purchase': True}
#     except ...:
#         return {'purchase': False}
#
#
# @app.route('/cancel-premium', methods=['GET'])
# def cancel_premium():
#     try:
#         if random.randint(0, 1) == 1:
#             return {'cancel': False}
#
#         client_id = request.args.get('id')
#         db_manager.cancel_premium_with_client_id(client_id=client_id)
#         return {'cancel': True}
#     except ...:
#         return {'cancel': False}
#
#
# @app.route('/upload-image-and-rate', methods=['POST'])
# def upload_image_and_rate():
#     try:
#         file = None
#         client_id = request.args.get('id')
#         is_male = bool(request.args.get('is_male'))
#         birthday = request.args.get('birthday')
#
#         if 'image' in request.files:
#             file = request.files['image']
#
#         if not file:
#             print('File is not here', file)
#             return {'images_to_rate': []}, 400
#
#         file_name = file.filename
#         if not file_name:
#             return jsonify({'error': 'No selected file'}), 400
#
#         user_id = db_manager.get_user_from_client_id(client_id=client_id, birthday=birthday, is_male=is_male)[0]
#
#         file_bytes = np.fromfile(file, dtype=np.uint8)
#         img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
#
#         file_extension = f'.{file_name.split(".")[-1]}'
#         session_img_path = get_new_image_path(user_id, file_extension)
#         cv.imwrite(session_img_path, img)
#         db_manager.create_new_image_record(user_id=user_id, is_male=is_male, img_format=file_extension)
#
#         return {'images_to_rate': girl_images}
#     except ...:
#         print('Error happend')
#         return {'images_to_rate': []}, 404


@app.route('/hi', methods=['GET'])
def upload_image_and_rate():
    return 'hellooooooo'
