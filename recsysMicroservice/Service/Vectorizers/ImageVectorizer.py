import torchvision.models as models
from torchvision.transforms import Resize
from torchvision.transforms import Normalize
from torchvision.transforms import ToTensor
from torch.autograd import Variable
import numpy as np
import torch
from PIL import Image


class ImageVectorizer:

    def __init__(self) -> None:
        self.__model = models.resnet18(pretrained=True)
        self.__scaler = Resize((224, 224))
        self.__normalize = Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
        self.__to_tensor = ToTensor()

        self.__layer = self.__model._modules.get('avgpool')

    def resnet_vectorize(self, img: Image.Image):
        if img.mode != 'RGB':
            img = img.convert('RGB')

        t_img = Variable(self.__normalize(self.__to_tensor(self.__scaler(img))).unsqueeze(0))
        embedding = torch.zeros(1, 512, 1, 1)

        def copy_data(m, i, o):
            embedding.copy_(o.data)

        h = self.__layer.register_forward_hook(copy_data)

        self.__model(t_img)

        h.remove()

        return np.array((embedding.squeeze().numpy()))
