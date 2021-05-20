import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch

W = torch.load('/home/tarek/PycharmProjects/breathe-out-api/model_6.pt')


def predict_fvc(intersect, base_week, current_week, features):
    features = torch.from_numpy(features)
    return intersect + (current_week - base_week) * (features @ W)
