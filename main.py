from PIL import Image, ImageDraw
from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def draw_circles_on_image(team_number, coordinates, color = (0, 134, 64)):
    dirname = os.path.dirname(__file__)
    image_path = "teams/" + str(team_number) + ".png"
    image_path = os.path.join(dirname, image_path)

    if not os.path.exists(image_path):
        reset_pic(team_number)

    # Open the image
    img = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Set the circle color
    circle_color = color  # Green color

    # Draw a 5-pixel green circle on each coordinate
    for coord in coordinates:
        x, y = coord
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=circle_color, outline=circle_color)

    # Save the modified image (overwriting the input image)
    img.save(image_path)

    print("image " + str(team_number) + " drawn successfully")

def draw_circles_on_pose_image(team_number, coordinates):
    dirname = os.path.dirname(__file__)
    image_path = "StartingPoses/" + str(team_number) + ".png"
    image_path = os.path.join(dirname, image_path)

    if not os.path.exists(image_path):
        reset_pic(team_number)

    # Open the image
    img = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Set the circle color
    circle_color = (129, 45, 207)  # Green color

    # Draw a 5-pixel green circle on each coordinate
    for coord in coordinates:
        x, y = coord
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=circle_color, outline=circle_color)

    # Save the modified image (overwriting the input image)
    img.save(image_path)

    print("pose image " + str(team_number) + " drawn successfully")


def reset_pic(team_number):
    # replace image with replacement_image_path
    dirname = os.path.dirname(__file__)
    image_path = "teams/" + str(team_number) + ".png"
    image_path = os.path.join(dirname, image_path)

    replacement_image_path = "emptyField.png"
    replacement_image_path = os.path.join(dirname, replacement_image_path)
    img = Image.open(replacement_image_path)

    img.save(image_path)

    # replace pose image with replacement_image_path
    pose_image_path = "StartingPoses/" + str(team_number) + ".png"
    pose_image_path = os.path.join(dirname, pose_image_path)

    pose_replacement_image_path = "emptyField.png"
    pose_replacement_image_path = os.path.join(dirname, pose_replacement_image_path)
    pose_img = Image.open(replacement_image_path)

    pose_img.save(pose_image_path)

    print("images for team " + str(team_number) + " reset successfully")


@app.route('/update_image', methods=['POST'])
def update_image():
    data = request.get_json()

    team_number = data['team_number']

    ScoreCoordinates = data.get('ScoreCoordinates', [])
    draw_circles_on_image(team_number, ScoreCoordinates, (0, 134, 64))
    MissCoordinates = data.get('MissCoordinates', [])
    draw_circles_on_image(team_number, MissCoordinates, (255, 217, 8))
    PoseCoordinates = data.get('PoseCoordinates', [])
    draw_circles_on_pose_image(team_number, PoseCoordinates)

    return jsonify({"message": "Request processed successfully"})

@app.route('/reset_image', methods=['POST'])
def reset_image():
    data = request.get_json()

    team_number = data['team_number']

    reset_pic(team_number)

    return jsonify({"message": "Request processed successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)