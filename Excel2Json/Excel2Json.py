import xlrd
import json
import os

class Excel2Json(object):

    def __init__(self,Excelpath):
        self.path = Excelpath
        self.table = xlrd.open_workbook(self.path).sheets()[0]
        self.nrows = self.table.nrows

print('test------------')
    def readTemplateAndWrite(self,targetpath,row,Jsonpath=r'./template/2.json'):

        with open(Jsonpath, 'r' ,encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
        with open(targetpath,'w' ,encoding='UTF-8') as dump_f:
            for col in range(1,9):
                originalStr = self.table.cell_value(row, col)
                if(len(originalStr)!=0):
                    str = originalStr[1:-1]
                    strlist = str.split(',')
                    if(col == 1):
                        for item in strlist:
                            load_dict['分析案例']['产品信息']['设备名称'].append(item)
                    elif (col == 2):
                        for item in strlist:
                            load_dict['分析案例']['产品信息']['部件名称'].append(item)
                    elif (col == 3):
                        for item in strlist:
                            load_dict['分析案例']['产品信息']['设计要求'].append(item)
                    elif (col == 4):
                        for item in strlist:
                            load_dict['分析案例']['目的信息'].append(item)
                    elif (col == 5):
                        for item in strlist:
                            load_dict['分析案例']['材料信息']["材料牌号"].append(item)
                    elif (col == 6):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            #if(len(temp)<2):
                            load_dict['分析案例']['材料信息']["材料属性"].append(temp[0])
                            # else:
                            #     load_dict['分析案例']['材料信息']["材料属性"].append({temp[0]:temp[1]})
                    elif (col == 7):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            #if (len(temp) < 2):
                            load_dict['分析案例']['工况']["设计工况"].append(temp[0])
                            # else:
                            #     load_dict['分析案例']['工况']["设计工况"].append({temp[0]:temp[1]})


                    elif (col == 8):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            #if (len(temp) < 2):
                            load_dict['分析案例']['工况']["工作工况"].append(temp[0])
                            # else:
                            #     load_dict['分析案例']['工况']["工作工况"].append({temp[0]:temp[1]})

            json.dump(load_dict,dump_f,ensure_ascii=False)
print('test------------')
    def readTemplateAndWriteE(self, targetpath, row, Jsonpath=r'./template/3.json'):

        with open(Jsonpath, 'r' ,encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
        with open(targetpath,'w' ,encoding='UTF-8') as dump_f:
            for col in range(1,9):
                originalStr = self.table.cell_value(row, col)
                if(len(originalStr)!=0):
                    str = originalStr[1:-1]
                    strlist = str.split(',')
                    if(col == 1):
                        for item in strlist:
                            load_dict['FEA task']['Product information']['Equipment name'].append(item)
                    elif (col == 2):
                        for item in strlist:
                            load_dict['FEA task']['Product information']['Part name'].append(item)
                    elif (col == 3):
                        for item in strlist:
                            load_dict['FEA task']['Product information']['Design requirement'].append(item)
                    elif (col == 4):
                        for item in strlist:
                            load_dict['FEA task']['Analysis aim'].append(item)
                    elif (col == 5):
                        for item in strlist:
                            load_dict['FEA task']['Material and physical data']["Material designation"].append(item)
                    elif (col == 6):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            # if(len(temp)<2):
                            load_dict['FEA task']['Material and physical data']["Material property"].append(temp[0])
                            # else:
                            #     load_dict['FEA task']['Material and physical data']["Material property"].append({temp[0]:temp[1]})
                    elif (col == 7):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            #if (len(temp) < 2):
                            load_dict['FEA task']['Working condition']["Design condition"].append(temp[0])
                            # else:
                            #     load_dict['FEA task']['Working condition']["Design condition"].append({temp[0]:temp[1]})


                    elif (col == 8):
                        for item in strlist:
                            # item : "xxxx:xxxx"
                            temp = item.split(':')
                            #if (len(temp) < 2):
                            load_dict['FEA task']['Working condition']["Operation condition"].append(temp[0])
                            # else:
                            #     load_dict['FEA task']['Working condition']["Operation condition"].append({temp[0]:temp[1]})

            json.dump(load_dict, dump_f)


def generate_chineseVersion_jsonFile(excelPath = r'./FEA案例数据_中文400.xlsx',targetRootPath = './result/c/'):
    example = Excel2Json(excelPath)
    if not os.path.exists(targetRootPath):
        os.makedirs(targetRootPath)
    count = 0
    for row in range(1, example.nrows, 1):
        targetPath = targetRootPath+str(count)+'.json'
        if not os.path.exists(targetPath):
            file = open(targetPath,'w')
            file.close()
        example.readTemplateAndWrite(targetPath,row)
        count+=1

def generate_EnglishVersion_jsonFile(excelPath = r'./FEA案例数据_英文400.xlsx',targetRootPath = './result/e/'):
    example = Excel2Json(excelPath)
    if not os.path.exists(targetRootPath):
        os.makedirs(targetRootPath)
    count = 0
    for row in range(2, example.nrows + 1, 1):
        targetPath = targetRootPath + str(count) + '.json'
        if not os.path.exists(targetPath):
            file = open(targetPath, 'w')
            file.close()
        example.readTemplateAndWriteE(targetPath, row)
        count += 1





if __name__ == '__main__':

    generate_chineseVersion_jsonFile()
    generate_EnglishVersion_jsonFile()

