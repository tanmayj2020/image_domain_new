from network import Resnet_Network
from torch import optim
import torch
import time
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def training_loss(criterion , output , ya ,  yb , lam):
    loss = lam * criterion(output , ya) + (1 - lam) * criterion(output , yb)
    print(loss)
    return loss
    
    

class Sketch_Classification(nn.Module):
    def __init__(self, hp):
        super(Sketch_Classification, self).__init__()
        self.Network = eval(hp.backbone_name + "_Network(hp)")
        self.train_params = self.parameters()
        self.optimizer = optim.Adam(self.train_params, hp.learning_rate)
        self.criterion = nn.CrossEntropyLoss()
        self.train_loss = training_loss
        self.hp = hp

    def train_model(self, batch):
        self.train()
        self.optimizer.zero_grad()
        output = self.Network(batch["sketch_img"].to(device))
        loss = self.train_loss(self.criterion , output, batch["sketch_label"].to(device) , batch["mixup_label"].to(device) , batch["lam"].to(device))
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def evaluate(self, dataloader_Test):
        self.eval()
        correct = 0
        test_loss = 0
        start_time = time.time()
        for i_batch, batch in enumerate(dataloader_Test):

            output = self.Network(batch["sketch_img"].to(device))
            test_loss += self.criterion(output, batch["sketch_label"].to(device)).item()
            prediction = output.argmax(dim=1, keepdim=True).to('cpu')
            correct += prediction.eq(batch['sketch_label'].view_as(prediction)).sum().item()
        
        test_loss /= len(dataloader_Test.dataset)
        accuracy = 100.0 * correct / len(dataloader_Test.dataset)

        print(
            "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%), Time_Takes: {}\n".format(
                test_loss,
                correct,
                len(dataloader_Test.dataset),
                accuracy,
                (time.time() - start_time),
            )
        )

        return accuracy
