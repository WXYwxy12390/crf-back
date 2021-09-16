import urllib.request
import urllib.parse
import json
import time
import base64

blood_routine_item_to_code = {'红细胞计数': 'RBC', '血红蛋白': 'HGb', '红细胞压积': 'HCT', '平均RBC体积': 'MCV',
                              '平均血红蛋白含量': 'MCH', '平均血红蛋白浓度': 'MCHC', 'RBC分布宽度CV': 'RDWCV', 'RBC分布宽度SD': 'RDWSD',
                              '白细胞计数': 'WBC',
                              '中性粒细胞(#)': 'GRAN_', '淋巴细胞(#)': 'LYM_', '嗜酸细胞(#)': 'EOS_', '单核细胞(#)': 'MID_',
                              '嗜碱细胞(#)': 'BASO_',
                              '血小板计数': 'PLT', '淋巴细胞(%)': 'LYM', '单核细胞(%)': 'MID', '中性粒细胞(%)': 'GRAN', '嗜酸细胞(%)': 'EOS',
                              '嗜碱细胞(%)': 'BASO'}
blood_bio_item_to_code = {'总蛋白': 'TP', '白蛋白': 'ALB', '球蛋白': 'GLO', '丙氨酸氨基转移酶': 'ALT', '门冬氨酸氨基转氨酶': 'AST',
                          '乳酸脱氢酶': 'LDH',
                          'γ-谷氨酰转肽酶': 'GGT', '总胆红素': 'TBIL', '直接胆红素': 'DBIL', '间接胆红素': 'IBIL', '血糖': 'GLU',
                          '总胆固醇': 'TC',
                          '低密度脂蛋白': 'LDL', '高密度脂蛋白': 'HDL', '甘油酸酯': 'TG', '尿素': 'UREA', '碱性磷酸酶': 'ALP', '肌酐': 'CREA',
                          '尿酸': 'UA', '二氧化碳': 'CO2', '钾': 'K', '钠': 'Na', '氯': 'Cl', '钙': 'Ca', '镁': 'Mg', '磷': 'P'}
thyroid_item_to_code = {'游离T3': 'FT3', '游离T4': 'FT4', '游离T3.': 'FT3', '游离T4.': 'FT4', '促甲状腺素': 'TSH', '促甲状腺素.': 'TSH'}

coagulation_item_to_code = {'凝血酶原时间': 'PT', '活化部分凝血活酶时间': 'APTT', '凝血酶时间': 'TT',
                            '纤维蛋白原': 'FIB', '国际标准化比值': 'INR', 'D-D二聚体定量': 'D_dimer'}

myocardial_enzyme_item_to_code = {'乳酸脱氢酶': 'LDH', '肌酸激酶': 'CK', '肌酸激酶同工酶': 'CK_MB', '肌酸激酶MB型同工酶': 'CK_MB',
                                  '高敏心肌肌钙蛋白I': 'cTnI', '超敏肌钙蛋白I': 'cTnT', '高敏心肌肌钙蛋白T': 'cTnT', '超敏肌钙蛋白T': 'cTnT',
                                  '肌红蛋白': 'MYO', '脑钠肽': 'BNP', '氨基末端脑钠肽前体': 'NT_proBNP'}

cytokines_item_to_code = {'肿瘤坏死因子α': 'TNF-a', '白细胞介素1β': 'IL_1b',
                          '白细胞介素2受体': 'IL_2R', '白细胞介素6': 'IL_6', '白细胞介素8': 'IL_8', '白细胞介素10': 'IL_10'}

lymSubsets_item_to_code = {'总B淋巴细胞(CD3-CD19+)(#)': 'CD19_', '总T淋巴细胞(CD3+CD19-)(#)': 'CD3_',
                           '总B淋巴细胞(CD3-CD19+)(%)': 'CD19', '总T淋巴细胞(CD3+CD19-)(%)': 'CD3',
                           '辅助/诱导性T淋巴细胞(CD3+CD4+)(#)': 'CD3_CD4__', '辅助/诱导性T淋巴细胞(CD3+CD4+)(%)': 'CD3_CD4_',
                           '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(#)': 'CD3_CD8__', '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(%)': 'CD3_CD8_',
                           'NK细胞(CD3-/CD16+CD56+)(#)': 'CD3_CD16_56_', 'NK细胞(CD3-/CD16+CD56+)(%)': 'CD3_CD16_56',
                           'Th/Ts': 'CD4CD8'}

urineRoutine_item_to_code = {'酸碱度': 'UPH', '尿葡萄糖': 'UGLU', '白细胞计数': 'LEU',
                             '红细胞计数': 'ERY', '亚硝酸盐': 'NIT', '尿胆红素': 'BIL', '比重': 'USG', '尿酮体': 'KET',
                             '尿隐血': 'BLD', '尿蛋白': 'PRO', '尿胆原': 'UBG', '尿颜色': 'COL', '尿透明度': 'CLA'}

tumorMarker_item_to_code = {'癌胚抗原': 'CEA', '神经元特异性烯醇化酶': 'NSE',
                            '胃泌素释放肽前体': 'pro-GPR', '鳞状细胞癌相关抗原': 'SCCA'}

lung_item_to_code = {}


def posturl(url, data={}):
    # 请求头
    headers = {
        'Authorization': 'APPCODE c7e50f3fd83244a2a2dde4c51ea32c30',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        params = json.dumps(data).encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html = r.read()
        r.close()
        return html.decode("utf8")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    time.sleep(1)


def ocr(path):
    with open(path, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data), 'utf-8')

    url_request = "https://ocrapi-advanced.taobao.com/ocrservice/advanced"
    dict = {'img': encodestr}

    html = posturl(url_request, data=dict)
    html_dic = json.loads(html)
    wordsInfo = html_dic.get('prism_wordsInfo')
    words = []
    for word in wordsInfo:
        words.append(word.get('word'))

    # print(html_dic)
    print(words)
    return words


def get_mea(value, normal_range):
    if '-' in normal_range:
        normal_range = normal_range.split('-')
        min_of_range = float(normal_range[0])
        max_of_range = float(normal_range[1])
        if min_of_range <= value <= max_of_range:
            return 0
        else:
            return 1
    elif '<' in normal_range:
        normal_range = normal_range.split('<')
        max_of_range = float(normal_range[1])
        if value < max_of_range:
            return 0
        else:
            return 1
    elif '≤' in normal_range:
        normal_range = normal_range.split('≤')
        max_of_range = float(normal_range[1])
        if value <= max_of_range:
            return 0
        else:
            return 1
    elif '>' in normal_range:
        normal_range = normal_range.split('>')
        min_of_range = float(normal_range[1])
        if value > min_of_range:
            return 0
        else:
            return 1
    elif '≥' in normal_range:
        normal_range = normal_range.split('≥')
        min_of_range = float(normal_range[1])
        if value >= min_of_range:
            return 0
        else:
            return 1


def lab_inspectation_ocr(path, table_name):
    items = ocr(path)
    data = {}
    ocr_py = __import__('app.utils.ocr', fromlist=['XXX'])
    item_to_code = getattr(ocr_py, table_name + '_item_to_code')
    map_keys = item_to_code.keys()
    for i in range(0, len(items)):
        item = items[i]
        if item in map_keys:
            code = item_to_code.get(item)
            # normal_range = items[i + 2]
            try:
                value = float(items[i + 1])
                data[code] = value
                # data[code + 'Mea'] = get_mea(value, normal_range)
            except ValueError:
                data[code] = None
                # value = items[i + 1]
                # if value[0] == normal_range[0]:
                #     data[code + 'Mea'] = 0
                # else:
                #     data[code + 'Mea'] = 1

    return data


# def ocr_crf(path):
#     words = ocr(path)
#     data = {}
#     folMet_map = {'电话': 1, '门诊': 2, '住院': '3'}
#     effEva_map = {'PD-进展': 1, 'PD': 1, '进展': 1,
#                   'SD-稳定': 2, 'SD': 2, '稳定': 2,
#                   'PR-部分缓解': 3, 'PR': 3, '部分缓解': 3,
#                   'CR-完全缓解': 4, 'CR': 4, '完全缓解': 4,
#                   '术后未发现新病': 5}
#     livSta_map = {'死亡': 1, '存活': 2, '失联': '3'}
#     imaFilType_map = {'X光': 1, 'x光': 1,
#                       '超声': 2, 'CT': 3,
#                       'MRI': 4,
#                       'PET': 5, 'PET/CT': 5}
#     imaFilTypes = ['X光', 'x光', '超声', 'CT', 'MRI', 'PET', 'PET/CT']
#     for word in words:
#         if '随访方式' in word:
#             for key, value in folMet_map:
#                 if key in word:
#                     data['forMet'] = value
#         elif '疗效评估' in word:
#             for key, value in effEva_map:
#                 if key in word:
#                     data['effEva'] = value
#         elif '生存状态' in word:
#             for key, value in livSta_map:
#                 if key in word:
#                     data['livSta'] = value
#         elif '影像类型' in word:
#             for value in imaFilTypes:
#                 if value in word:
#                     data['imaFilType'] = imaFilType_map.get(value)
#         elif '随访日期' in word:
#             pass
#         elif '备注' in word:
#             pass
#         elif '死亡时间' in word:
#             pass
#
#     return data


if __name__ == "__main__":
    # ocr('C:/Users/dell/Desktop/fsdownload/blood_routine/微信图片_20201118152459.jpg')

    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/blood_routine/微信图片_20201118152459.jpg','blood_routine'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/blood_bio/微信图片_20201208153935.jpg', 'blood_bio'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/thyroid/微信图片_20201225123222.jpg', 'thyroid'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/coagulation/微信图片_20201216153633.jpg', 'coagulation'))
    print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/myocardialEnzyme/2019.06.15.jpg', 'myocardial_enzyme'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/cytokines/微信图片_20201108145817.jpg', 'cytokines'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/lymSubsets/微信图片_20201108104503.jpg', 'lymSubsets'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/urineRoutine/25.jpg', 'urineRoutine'))
    # print(lab_inspectation_ocr('C:/Users/dell/Desktop/fsdownload/tumorMarker/微信图片_20201225153143.jpg', 'tumorMarker'))
