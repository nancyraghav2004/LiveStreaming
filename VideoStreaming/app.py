from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0) #We should be able to access our webcam in order to acess our webcam we will use cv2
#When we pass 0 , bydefault it is our camera

def generate_frames():
    #So this function will do is, first we will try to read that canera = cv2.. here
    while True:
        success,frame=camera.read()
        #When we try to read, it returns two parameters, first parameter is either we are getting any kind of frames or not
        #if we are getting frames, it will be success.
        #And success here is boolean value, if it is true , we will read it from camera.
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg',frame) #so I am here, trying to to read frame, and if it is true like if I am 
            #actually getting frames (from frame=camera.read) than i will try to encode the frames (cv.imencode(...) and converting it into jpg)
            #And it will return two things, one variable will be ret and other will be buffer
            frame = buffer.tobytes()
            #we are not using return keyword because it will capture some images and will return to the function
            #things won't be in cont. manner
            #If i write return frame, so things won't work out. it will read one frame ans it will give to function anf will not go back
            #so in order to go back over here, one keyword we can use is yield (we use it along with the generator)
            yield(b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #SO i am passing the frames here, so it will come back to function, select next frames and give it back
            #But before sending the frames, we really need to select some more features in it
            #features are something called as content type where we are giving the image extension



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    #This function will return something, so we have to do is we will make some html content
    #and html content should be able to hit this particular url to take the streaming data inindex.html
    #From this function, we need to pass some response, for that we are using Response library
    #This response is some kind of response that I am actually trying to send in a cont. manner
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    #This response will call some function, and this function will be generating or will be taking the frames from my webcam
    #And it will pass this entire response back to this index.html
    
if __name__ == "__main__":
    app.run(debug=True)



