import glob
import rosbag
import sys
from rosbag.bag import Bag
import time
import sklearn.model_selection as select
class_names = ['boxing', 'wave', 'jack', 'jump', 'walk', 'squats']
#(数据集的路径)
bag_path = './bag/'
#(输出保存的路径)
save_path = './to_txt/'
#(训练集的比例)
proportion = 0.8

def status(length, percent):
    sys.stdout.write('\x1B[2K')  # Erase entire current line
    sys.stdout.write('\x1B[0E')  # Move to the beginning of the current line
    progress = "Progress: ["
    for i in range(0, length):
        if i < length * percent:
            progress += '='
        else:
            progress += ' '
    progress += "] " + str(round(percent * 100.0, 2)) + "%"
    sys.stdout.write(progress)
    sys.stdout.flush()
def Bag_Record(classname):
    filesPath = glob.glob(bag_path+classname+"*.bag")
    topicCnts = 0
    for filePath in filesPath:
        bag = rosbag.Bag(filePath)
        topicCnts += bag.get_message_count('/ti_mmwave/radar_scan')
    train_f = open(save_path + 'train/' + classname + '.txt', mode='w')
    test_f  = open(save_path + 'test/'  + classname + '.txt', mode='w')
    train = True
    topicIndex = 0
    splitArray = [i for i in range(topicCnts)]
    trainIndex, testIndex = select.train_test_split(splitArray, train_size = proportion)
    dataIndex = [0]*topicCnts
    for i in testIndex:
        dataIndex[i] = 1
    for filePath in filesPath:
        bag = rosbag.Bag(filePath)
        for topic, msg, t in bag.read_messages(topics=['/ti_mmwave/radar_scan']):
            percent =  topicIndex / (1.0*topicCnts)
            status(40, percent)
            if(dataIndex[topicIndex] == 1):
                test_f.write(str(msg))
                test_f.write('\n')
            else:
                train_f.write(str(msg))
                train_f.write('\n')
            topicIndex += 1
    train_f.close()
    test_f.close()
    bag.close()
    print(classname)

if __name__ == '__main__':
  for name in class_names:
    Bag_Record(name)
