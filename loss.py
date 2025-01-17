import torch
import torch.nn as nn
import torch.nn.functional as F

class lossAV(nn.Module):
	def __init__(self):
		super(lossAV, self).__init__()
		self.criterion = nn.BCELoss()
		self.FC        = nn.Linear(128, 2)
		
	def forward(self, x, labels = None, r = 1):	
		x = x.squeeze(1)
		x = self.FC(x)
		if labels == None:
			predScore = x[:,1]
			predScore = predScore.t()
			predScore = predScore.view(-1).detach().cpu().numpy()
			return predScore
		if labels == 'probability':
			x1 = x / r
			predScore = F.softmax(x, dim = -1)
			predScore = predScore.view(-1).detach().cpu().numpy()
			return predScore   #这里得到的就是说话概率
		else:
			x1 = x / r
			x1 = F.softmax(x1, dim = -1)[:,1]
			nloss = self.criterion(x1, labels.float())
			predScore = F.softmax(x, dim = -1)
			predLabel = torch.round(F.softmax(x, dim = -1))[:,1]   #这里四舍五入就是当说话概率大于0.5时，直接标为1
			print("----------------------------------")
			print(len(labels))
			print(len(predLabel))
			correctNum = (predLabel == labels).sum().float()
			return nloss, predScore, predLabel, correctNum


class lossV(nn.Module):
	def __init__(self):
		super(lossV, self).__init__()
		self.criterion = nn.BCELoss()
		self.FC        = nn.Linear(128, 2)

	def forward(self, x, labels, r = 1):	
		x = x.squeeze(1)
		x = self.FC(x)
		
		x = x / r
		x = F.softmax(x, dim = -1)

		nloss = self.criterion(x[:,1], labels.float())
		return nloss