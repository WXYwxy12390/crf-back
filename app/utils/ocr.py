import urllib.request
import urllib.parse
import json
import time
import base64

BloodRoutine_item_to_code = {
    '红细胞计数': 'RBC', '血红蛋白': 'HGb', '红细胞压积': 'HCT', '平均RBC体积': 'MCV', '血小板计数': 'PLT',
    '平均血红蛋白含量': 'MCH', '平均血红蛋白浓度': 'MCHC', 'RBC分布宽度CV': 'RDWCV', '白细胞计数': 'WBC',
    'RBC分布宽度SD': 'RDWSD', 'RBC分布宽度5D': 'RDWSD',
    '中性粒细胞(#)': 'GRAN_', '中性粒细胞#)': 'GRAN_', '中性粒细胞(#': 'GRAN_', '中性粒细胞#': 'GRAN_',
    '淋巴细胞(#)': 'LYM_', '淋巴细胞#)': 'LYM_', '淋巴细胞(#': 'LYM_', '淋巴细胞#': 'LYM_',
    '嗜酸细胞(#)': 'EOS_', '嗜酸细胞#)': 'EOS_', '嗜酸细胞(#': 'EOS_', '嗜酸细胞#': 'EOS_',
    '单核细胞(#)': 'MID_', '单核细胞#)': 'MID_', '单核细胞(#': 'MID_', '单核细胞#': 'MID_',
    '嗜碱细胞(#)': 'BASO_', '嗜碱细胞#)': 'BASO_', '嗜碱细胞(#': 'BASO_', '嗜碱细胞#': 'BASO_',
    '淋巴细胞(%)': 'LYM', '淋巴细胞%)': 'LYM', '淋巴细胞(%': 'LYM', '淋巴细胞%': 'LYM',
    '单核细胞(%)': 'MID', '单核细胞%)': 'MID', '单核细胞(%': 'MID', '单核细胞%': 'MID',
    '中性粒细胞(%)': 'GRAN', '中性粒细胞%)': 'GRAN', '中性粒细胞(%': 'GRAN', '中性粒细胞%': 'GRAN',
    '嗜酸细胞(%)': 'EOS', '嗜酸细胞%)': 'EOS', '嗜酸细胞(%': 'EOS', '嗜酸细胞%': 'EOS',
    '嗜碱细胞(%)': 'BASO', '嗜碱细胞%)': 'BASO', '嗜碱细胞(%': 'BASO', '嗜碱细胞%': 'BASO',
}
BloodBio_item_to_code = {
    '总蛋白': 'TP', '白蛋白': 'ALB', '球蛋白': 'GLO', '丙氨酸氨基转移酶': 'ALT', '门冬氨酸氨基转氨酶': 'AST',
    '乳酸脱氢酶': 'LDH', '总胆红素': 'TBIL', '直接胆红素': 'DBIL', '间接胆红素': 'IBIL', '血糖': 'GLU',
    'γ-谷氨酰转肽酶': 'GGT', 'γ谷氨酰转肽酶': 'GGT', 'v-谷氨酰转肽酶': 'GGT', 'v谷氨酰转肽酶': 'GGT', 'y-谷氨酰转肽酶': 'GGT', 'y谷氨酰转肽酶': 'GGT',
    '总胆固醇': 'TC', '低密度脂蛋白': 'LDL', '高密度脂蛋白': 'HDL', '甘油酸酯': 'TG', '尿素': 'UREA', '碱性磷酸酶': 'ALP',
    '肌酐': 'CREA', '尿酸': 'UA', '二氧化碳': 'CO2', '钾': 'K', '钠': 'Na', '氯': 'Cl', '钙': 'Ca', '镁': 'Mg', '磷': 'P'
}
Thyroid_item_to_code = {
    '游离T3': 'FT3', '游离T3.': 'FT3', '游离三碘甲状腺素': 'FT3',
    '游离T4': 'FT4', '游离T4.': 'FT4', '游离甲状腺素': 'FT4',
    '促甲状腺素': 'TSH', '促甲状腺素.': 'TSH', '促甲状腺激素': 'TSH'
}

Coagulation_item_to_code = {
    '凝血酶原时间': 'PT', '活化部分凝血活酶时间': 'APTT', '凝血酶时间': 'TT',
    '纤维蛋白原': 'FIB', '国际标准化比值': 'INR', 'D-D二聚体定量': 'D_dimer'
}

MyocardialEnzyme_item_to_code = {
    '乳酸脱氢酶': 'LDH', '肌酸激酶': 'CK',
    '肌酸激酶同工酶': 'CK_MB', '肌酸激酶MB型同工酶': 'CK_MB',
    '高敏心肌肌钙蛋白I': 'cTnI', '超敏肌钙蛋白I': 'cTnI',
    '高敏心肌肌钙蛋白T': 'cTnT', '超敏肌钙蛋白T': 'cTnT',
    '肌红蛋白': 'MYO', '脑钠肽': 'BNP', '氨基末端脑钠肽前体': 'NT_proBNP'
}

Cytokines_item_to_code = {
    '肿瘤坏死因子α': 'TNF-a', '肿瘤坏死因子a': 'TNF-a',
    '白细胞介素1β': 'IL_1b', '白细胞介素1B': 'IL_1b',
    '白细胞介素2受体': 'IL_2R', '白细胞介素6': 'IL_6', '白细胞介素8': 'IL_8', '白细胞介素10': 'IL_10'
}

LymSubsets_item_to_code = {
    '总B淋巴细胞(CD3-CD19+)(#)': 'CD19_', '总B巴细胞(CD3-CD19+)(#)': 'CD19_', '总B淋巴细胞(CD3-CD19+)#)': 'CD19_', '总B巴细胞(CD3-CD19+)#)': 'CD19_',
    '总B淋巴细胞(CD3-CD19+)(#': 'CD19_', '总B巴细胞(CD3-CD19+)(#': 'CD19_', '总B淋巴细胞(CD3-CD19+)#': 'CD19_', '总B巴细胞(CD3-CD19+)#': 'CD19_',

    '总T淋巴细胞(CD3+CD19-)(#)': 'CD3_', '总T巴细胞(CD3+CD19-)(#)': 'CD3_', '总T淋巴细胞(CD3+CD19-)#)': 'CD3_', '总T巴细胞(CD3+CD19-)#)': 'CD3_',
    '总T淋巴细胞(CD3+CD19-)#': 'CD3_', '总T巴细胞(CD3+CD19-)#': 'CD3_', '总T淋巴细胞(CD3+CD19-)(#': 'CD3_', '总T巴细胞(CD3+CD19-)(#': 'CD3_',

    '总B淋巴细胞(CD3-CD19+)(%)': 'CD19', '总B巴细胞(CD3-CD19+)(%)': 'CD19', '总B淋巴细胞(CD3-CD19+)%)': 'CD19', '总B巴细胞(CD3-CD19+)%)': 'CD19',
    '总B淋巴细胞(CD3-CD19+)(%': 'CD19', '总B巴细胞(CD3-CD19+)(%': 'CD19', '总B淋巴细胞(CD3-CD19+)%': 'CD19', '总B巴细胞(CD3-CD19+)%': 'CD19',

    '总T淋巴细胞(CD3+CD19-)(%)': 'CD3', '总T巴细胞(CD3+CD19-)(%)': 'CD3', '总T淋巴细胞(CD3+CD19-)%)': 'CD3', '总T巴细胞(CD3+CD19-)%)': 'CD3',
    '总T淋巴细胞(CD3+CD19-)(%': 'CD3', '总T巴细胞(CD3+CD19-)(%': 'CD3', '总T淋巴细胞(CD3+CD19-)%': 'CD3', '总T巴细胞(CD3+CD19-)%': 'CD3',

    '辅助/诱导性T淋巴细胞(CD3+CD4+)(#)': 'CD3_CD4__', '辅助/诱导性T巴细胞(CD3+CD4+)(#)': 'CD3_CD4__',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)#)': 'CD3_CD4__', '辅助/诱导性T巴细胞(CD3+CD4+)#)': 'CD3_CD4__',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)(#': 'CD3_CD4__', '辅助/诱导性T巴细胞(CD3+CD4+)(#': 'CD3_CD4__',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)#': 'CD3_CD4__', '辅助/诱导性T巴细胞(CD3+CD4+)#': 'CD3_CD4__',

    '辅助/诱导性T淋巴细胞(CD3+CD4+)(%)': 'CD3_CD4_', '辅助/诱导性T巴细胞(CD3+CD4+)(%)': 'CD3_CD4_',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)%)': 'CD3_CD4_', '辅助/诱导性T巴细胞(CD3+CD4+)%)': 'CD3_CD4_',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)(%': 'CD3_CD4_', '辅助/诱导性T巴细胞(CD3+CD4+)(%': 'CD3_CD4_',
    '辅助/诱导性T淋巴细胞(CD3+CD4+)%': 'CD3_CD4_', '辅助/诱导性T巴细胞(CD3+CD4+)%': 'CD3_CD4_',

    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(#)': 'CD3_CD8__', '抑制/细胞毒性T巴细胞(CD3+CD8+)(#)': 'CD3_CD8__',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)#)': 'CD3_CD8__', '抑制/细胞毒性T巴细胞(CD3+CD8+)#)': 'CD3_CD8__',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(#': 'CD3_CD8__', '抑制/细胞毒性T巴细胞(CD3+CD8+)(#': 'CD3_CD8__',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)#': 'CD3_CD8__', '抑制/细胞毒性T巴细胞(CD3+CD8+)#': 'CD3_CD8__',

    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(%)': 'CD3_CD8_', '抑制/细胞毒性T巴细胞(CD3+CD8+)(%)': 'CD3_CD8_',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)%)': 'CD3_CD8_', '抑制/细胞毒性T巴细胞(CD3+CD8+)%)': 'CD3_CD8_',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)(%': 'CD3_CD8_', '抑制/细胞毒性T巴细胞(CD3+CD8+)(%': 'CD3_CD8_',
    '抑制/细胞毒性T淋巴细胞(CD3+CD8+)%': 'CD3_CD8_', '抑制/细胞毒性T巴细胞(CD3+CD8+)%': 'CD3_CD8_',

    'NK细胞(CD3-/CD16+CD56+)(#)': 'CD3_CD16_56_', 'NK细胞(CD3-/CD16+CD56+)#)': 'CD3_CD16_56_',
    'NK细胞(CD3-/CD16+CD56+)(#': 'CD3_CD16_56_', 'NK细胞(CD3-/CD16+CD56+)#': 'CD3_CD16_56_',

    'NK细胞(CD3-/CD16+CD56+)(%)': 'CD3_CD16_56', 'NK细胞(CD3-/CD16+CD56+)%)': 'CD3_CD16_56',
    'NK细胞(CD3-/CD16+CD56+)(%': 'CD3_CD16_56', 'NK细胞(CD3-/CD16+CD56+)%': 'CD3_CD16_56',

    'Th/Ts': 'CD4CD8'
}

UrineRoutine_item_to_code = {
    '酸碱度': 'UPH', '尿葡萄糖': 'UGLU', '白细胞计数': 'LEU',
    '红细胞计数': 'ERY', '亚硝酸盐': 'NIT', '尿胆红素': 'BIL', '比重': 'USG', '尿酮体': 'KET',
    '尿隐血': 'BLD', '尿蛋白': 'PRO', '尿胆原': 'UBG', '尿颜色': 'COL', '尿透明度': 'CLA'
}

TumorMarker_item_to_code = {
    '癌胚抗原': 'CEA', '胃泌素释放肽前体': 'pro_GPR', 'CYFRA21-1': 'CYFRA', '铁蛋白': 'FERR', '甲胎蛋白': 'AFP',
    '神经元特异性烯醇化酶': 'NSE', '神经元特异烯醇化酶': 'NSE',
    '鳞状细胞癌相关抗原': 'SCCA', '鲜状细胞癌相关抗原': 'SCCA'
}

# Lung_item_to_code = {'FVC': 'FVC',
#                      'FEV1/FVC': 'FEV1_FVC', 'FEV 1%FVC': 'FEV1_FVC',
#                      'MEF': 'MEF', 'MEF25': 'MEF25', 'MEF50': 'MEF50', 'MEF75': 'MEF75',
#                      'TLC-sb': 'TLC_sb', "RV'": 'RV'}


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


def ocr_path(path):
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

    print(words)
    return words


def ocr_file(file):
    f = file.read()
    encodestr = str(base64.b64encode(f), 'utf-8')

    url_request = "https://ocrapi-advanced.taobao.com/ocrservice/advanced"
    dict = {'img': encodestr}

    html = posturl(url_request, data=dict)
    html_dic = json.loads(html)
    wordsInfo = html_dic.get('prism_wordsInfo')
    words = []
    for word in wordsInfo:
        words.append(word.get('word'))

    print(words)
    return words


def lab_inspectation_ocr(file, table_name):
    # items = ocr_path(path)
    items = ocr_file(file)
    data = {}
    ocr_py = __import__('app.utils.ocr', fromlist=['XXX'])
    item_to_code = getattr(ocr_py, table_name + '_item_to_code')
    map_keys = item_to_code.keys()
    for i in range(0, len(items)):
        item = items[i]
        if item in map_keys:
            code = item_to_code.get(item)
            print(item + ';' + code + ';' + items[i + 1])
            try:
                if table_name == 'UrineRoutine':
                    value = items[i + 1]
                else:
                    value = float(items[i + 1])
                data[code] = value
            except ValueError as err:
                print(str(err))
    return data


# if __name__ == "__main__":
    # ocr_path('D:\Downloads\医院报告单模版汇总\moleDetec\复旦大学附属中山医院病理科-病理诊断报告单.jpeg')
