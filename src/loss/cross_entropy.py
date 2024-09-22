import torch.nn as nn


class CrossEntropyLoss(nn.Module):
    def __init__(self):
        super(CrossEntropyLoss, self).__init__()
        self.base_ce = nn.CrossEntropyLoss()

    def forward(self, inputs, targets):
        return self.base_ce(inputs, targets)
