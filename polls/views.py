from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import time
count = 1
import tensorflow as tf, sys

from django.shortcuts import render

# Create your views here.
@csrf_exempt
def index(request):
    # request.send_header('Access-Control-Allow-Origin', '*')
    # get the image by name can be changed

    # if image name requested
    requestedImage = request.GET.get('image', False)

    base64_image_str = request.POST.get('croppedImage', False)
    filename = "no File"
    if base64_image_str:
        # change base64 to image string else that line do nothing
        base64_image_str = base64_image_str[base64_image_str.find(",") + 1:]

        # decode string
        imgdata = base64.b64decode(base64_image_str)

        # timestamp = total_seconds()


    # give unique file name and save in DB
        dt = time.time()
        filename = str(dt) + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)


    # ################################################
        image_path = filename
        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line
                    in tf.gfile.GFile("output_labels.txt")]

        # Unpersists graph from file
        with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            print(top_k)
        obj_list = []
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            obj_list.append({human_string: score})
            # print('%s (score = %.5f)' % (human_string, score))

        return HttpResponse(obj_list)




    # ################################################


    #     return response
    # return HttpResponse("Hello, world. You're at the polls index.")

    # fsock = open("1487426109.6448364.jpg", "rb")
    # return HttpResponse(fsock)
    if requestedImage:
        try:
            with open(requestedImage, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except IOError:
            return HttpResponse("sorry request image not found")
    else:
        return HttpResponse("Operation up and running " + filename )