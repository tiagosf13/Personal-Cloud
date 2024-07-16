from handlers.DatabaseHandler import get_current_dir


# Function to insert an image record into the database
def save_image(user_id, image_data=None):
    try:
        # Save the image in the static/images directory
        with open(get_current_dir(subdirectory="static/images/"+user_id+".png"), 'wb') as file:
            file.write(image_data)
        file.close()
        return True
    except Exception as e:
        print(e)
        return False