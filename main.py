from PIL import Image, ImageDraw
from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def DrawShootingPoses(team_number, coordinates, round_number, color):
    # all-time image
    dirname = os.path.dirname(__file__)
    image_path = "DCMP/ShootingPoses/" + str(team_number) + "/0.png"
    image_path = os.path.join(dirname, image_path)

    if not os.path.exists(image_path):
        reset_pic(team_number, 0) # if the image does not exist, create empty image

    img = Image.open(image_path) # Open the image

    draw = ImageDraw.Draw(img) # Create a drawing object

    circle_color = color # Set the circle color

    for coord in coordinates:
        x, y = coord
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=circle_color, outline=circle_color) # Draw a 5-pixel green circle on each coordinate

    img.save(image_path) # Save the modified image (overwriting the input image)


    # round specific image ========================================================================================================
    image_path = "DCMP/ShootingPoses/" + str(team_number) + "/" + str(round_number) + ".png"
    image_path = os.path.join(dirname, image_path)

    if not os.path.exists(image_path):
        reset_pic(team_number, round_number) # if the image does not exist, create empty image
    
    img = Image.open(image_path) # Open the image

    draw = ImageDraw.Draw(img) # Create a drawing object

    circle_color = color # Set the circle color

    for coord in coordinates:
        x, y = coord
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=circle_color, outline=circle_color) # Draw a 5-pixel green circle on each coordinate

    img.save(image_path) # Save the modified image (overwriting the input image)

    print("image " + str(team_number) + " drawn successfully")

def DrawStartingPoses(team_number, coordinates):
    dirname = os.path.dirname(__file__)
    image_path = "DCMP/StartingPoses/" + str(team_number) + ".png"
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

def reset_pic(team_number, round_number):
    # Define the base directory
    base_dir = os.path.dirname(__file__)

    # Create the folder for ShootingPoses if it doesn't exist
    shooting_poses_dir = os.path.join(base_dir, "DCMP/ShootingPoses", str(team_number))
    os.makedirs(shooting_poses_dir, exist_ok=True)

    # Create the folder for StartingPoses if it doesn't exist
    starting_poses_dir = os.path.join(base_dir, "DCMP/StartingPoses")
    os.makedirs(starting_poses_dir, exist_ok=True)

    # Construct the image path for ShootingPoses
    image_path = os.path.join(shooting_poses_dir, str(round_number) + ".png")

    # Construct the image path for StartingPoses
    pose_image_path = os.path.join(starting_poses_dir, str(team_number) + ".png")

    # Load replacement image
    replacement_image_path = os.path.join(base_dir, "emptyField.png")
    img = Image.open(replacement_image_path)

    # Save the replacement image for ShootingPoses
    img.save(image_path)

    # Save the replacement image for StartingPoses
    pose_img = Image.open(replacement_image_path)
    pose_img.save(pose_image_path)

    print("Images for team " + str(team_number) + " reset successfully")

@app.route('/update_image', methods=['POST'])
def update_image():
    data = request.get_json()

    team_number = data['team_number']

    round_number = data['round_number']

    ScoreCoordinates = data.get('ScoreCoordinates', [])
    DrawShootingPoses(team_number, ScoreCoordinates, round_number, (0, 134, 64))
    MissCoordinates = data.get('MissCoordinates', [])
    DrawShootingPoses(team_number, MissCoordinates, round_number, (255, 217, 8))
    PoseCoordinates = data.get('PoseCoordinates', [])
    DrawStartingPoses(team_number, PoseCoordinates)

    return jsonify({"message": "Request processed successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)