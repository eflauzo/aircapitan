import torch
from torch import nn
# from sklearn.metrics import r2_score
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import numpy as np
# import ball_sim
import math


class SimModel(nn.Module):
    def __init__(self, n_input_params, n_ouptut_params):
        super().__init__()
        n_hidden = n_input_params * 4
        self.fc1 = nn.Linear(n_input_params, n_hidden)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(n_hidden, n_hidden)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(n_hidden, n_ouptut_params)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


def eng2norm(ch_val, ch_range):
    ch_range_min, ch_range_max = ch_range
    return (ch_val - ch_range_min) / (ch_range_max - ch_range_min) * 2.0 - 1.0


class Sim2AI:
    def __init__(self, data_rec, state_channels, control_channels):
        self.data_rec = data_rec
        self.state_channels = state_channels
        self.control_channels = control_channels
        self.model = SimModel(len(self.state_channels),
                              len(self.control_channels))
        df = self.data_rec.as_df()

        prew_row = None

        self.input_channels = self.state_channels + self.control_channels
        self.output_channels = self.state_channels[:]

        self.inputs = []
        self.outputs = []

        for index, row in df.iterrows():
            if prew_row is not None:
                input_vals = []
                output_vals = []

                for ch, ch_range in self.input_channels:
                    input_vals.append(eng2norm(prew_row[ch], ch_range))

                for ch, ch_range in self.output_channels:
                    output_vals.append(eng2norm(row[ch], ch_range))

                    # for ch, ch_range in self.state_channels:
                    #    prew_vals.append(eng2norm(prew_row[ch], ch_range))
                    #    curr_vals.append(eng2norm(row[ch], ch_range))

                self.inputs.append(input_vals)
                self.outputs.append(output_vals)

                # print('--')
                # print(self.inputs)
                # print(self.outputs)
                # exit(1)
            prew_row = row

        inputs_tensor = torch.tensor(self.inputs, dtype=torch.float32)
        outputs_tensor = torch.tensor(self.outputs, dtype=torch.float32)

        # print(self.inputs)
        model = SimModel(len(self.input_channels),
                         len(self.output_channels))

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        # print('x')
        model.train()
        for epoch in range(10):
            outputs = model(inputs_tensor).squeeze()
            loss = criterion(outputs, outputs_tensor)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # print(index, row['A'], row['B'])

    # def train():

        model.eval()
