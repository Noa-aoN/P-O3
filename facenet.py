# Pip install Jupyter
# Pip install facenet-pytorch
# Type jupyter notebook in terminal
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

imagesize = 160
margin = 0.2

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=imagesize, margin=margin)
# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def get_embedding(imagepath):
    if isinstance(imagepath, str):
        img = Image.open(imagepath)
    else:
        img = imagepath
    img_cropped = mtcnn(img)
    img_embedding = resnet(img_cropped.unsqueeze(0))
    return img_embedding


def embeddingmatching(image1, image2):
    image1_embedding = get_embedding(image1)
    image2_embedding = get_embedding(image2)

    return image1_embedding @ image2_embedding.T


Bram1 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Bram3.jpg")
Bram2 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Bram5.jpg")
Gorjan1 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Gorjan1.jpg")


print(embeddingmatching(Bram1, Bram2))


