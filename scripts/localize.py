import cv2

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    # read image with opencv
    img = cv2.imread(path)

    # get height and width
    height, width, _ = img.shape

    vlist = [0,0,0,0,0,0,0,0]

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        i = 0;
        for vertex in object_.bounding_poly.normalized_vertices:
            vlist[i] = vertex.x
            vlist[i + 1] = vertex.y
            i = i + 2
            print(' - ({}, {})'.format(vertex.x, vertex.y))

        x1 = int(vlist[0] * width)
        y1 = int(vlist[1] * height)
        x2 = int(vlist[4] * width)
        y2 = int(vlist[5] * height)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)

    cv2.imwrite("parkinglot.png",img)

    cv2.imshow("lalala", img)
    k = cv2.waitKey(0) # 0==wait forever

    print(vlist)

   

filepath = input("Enter filename: ")

localize_objects("resources/" + filepath)


