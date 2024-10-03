from io import BytesIO
import unittest

from PIL import Image
import requests
from recsysMicroservice.Service.Vectorizers.ImageVectorizer import ImageVectorizer
import yaml

with open("./recsysMicroservice/config.yml", "r") as file:
    config = yaml.safe_load(file)

class ImageVectorizerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._vectorizer = ImageVectorizer()


    def test_vectorize_image(self):
        image_url = "https://i.ytimg.com/vi/1R9yAB5bE6s/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAWSVeV6mChwb9NxHHcmWjqi_Zkkw"
        with Image.open(BytesIO(requests.get(image_url).content)) as im:
            vector = self.__class__._vectorizer.resnet_vectorize(im)

        self.assertEqual(len(vector), config['Vectors']['IMAGE'], "Length of image vector must be {}".format(config['Vectors']['IMAGE']))


if __name__ == '__main__':
    unittest.main()
