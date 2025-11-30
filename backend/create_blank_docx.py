#!/usr/bin/env python3
"""
创建简单的空白DOCX文件
DOCX文件本质上是一个ZIP压缩包，包含XML文件
"""

import zipfile
import os
from datetime import datetime

def create_minimal_docx(filename="基础模板.docx"):
    """创建最小可用的DOCX文件"""

    # 创建目录结构
    docx_structure = {
        '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''',

        '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''',

        'word/_rels/document.xml.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',

        'word/document.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Title"/>
            </w:pPr>
            <w:r>
                <w:t>文档标题</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>这是一个基础模板，适用于一般的文档转换。您可以删除此内容并使用自己的Markdown文件。</w:t>
            </w:r>
        </w:p>
    </w:body>
</w:document>''',

        'word/styles.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:docDefaults>
        <w:rPrDefault>
            <w:rPr>
                <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hAnsi="宋体"/>
                <w:sz w:val="22"/>
                <w:szCs w:val="22"/>
            </w:rPr>
        </w:rPrDefault>
    </w:docDefaults>
    <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="0" w:defUnhideWhenUsed="0" w:defQFormat="0" w:priority="99" w:semiHidden="0" w:unhideWhenUsed="0" w:uiPriority="0" w:qFormat="0">
        <w:lsdException w:name="Normal" w:semiHidden="0" w:uiPriority="0" w:unhideWhenUsed="0" w:qFormat="1"/>
        <w:lsdException w:name="heading 1" w:semiHidden="0" w:uiPriority="9" w:unhideWhenUsed="0" w:qFormat="1"/>
        <w:lsdException w:name="heading 2" w:uiPriority="9" w:qFormat="1"/>
    </w:latentStyles>
    <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:spacing w:after="0" w:line="240" w:lineRule="auto"/>
        </w:pPr>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hAnsi="宋体" w:cs="宋体"/>
            <w:sz w:val="22"/>
            <w:szCs w:val="22"/>
        </w:rPr>
    </w:style>
    <w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">
        <w:name w:val="Default Paragraph Font"/>
        <w:uiPriority w:val="1"/>
        <w:semiHidden w:val="0"/>
        <w:unhideWhenUsed w:val="0"/>
    </w:style>
    <w:style w:type="table" w:default="1" w:styleId="TableNormal">
        <w:name w:val="Normal Table"/>
        <w:uiPriority w:val="99"/>
        <w:semiHidden w:val="0"/>
        <w:unhideWhenUsed w:val="0"/>
        <w:tblPr>
            <w:tblInd w:w="0" w:type="dxa"/>
            <w:tblCellMar>
                <w:top w:w="0" w:type="dxa"/>
                <w:left w:w="108" w:type="dxa"/>
                <w:bottom w:w="0" w:type="dxa"/>
                <w:right w:w="108" w:type="dxa"/>
            </w:tblCellMar>
        </w:tblPr>
    </w:style>
    <w:style w:type="numbering" w:default="1" w:styleId="ListParagraph">
        <w:name w:val="List Paragraph"/>
        <w:uiPriority w:val="34"/>
        <w:semiHidden w:val="0"/>
        <w:unhideWhenUsed w:val="0"/>
        <w:pPr>
            <w:ind w:left="432"/>
        </w:pPr>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Title">
        <w:name w:val="Title"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:link w:val="TitleChar"/>
        <w:uiPriority w:val="10"/>
        <w:qFormat/>
        <w:pPr>
            <w:spacing w:before="240" w:after="0"/>
            <w:jc w:val="center"/>
            <w:outlineLvl w:val="0"/>
        </w:pPr>
        <w:rPr>
            <w:rFonts w:ascii="黑体" w:eastAsia="黑体" w:hAnsi="黑体"/>
            <w:b/>
            <w:bCs/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:style>
    <w:style w:type="character" w:customStyle="1" w:styleId="TitleChar">
        <w:name w:val="Title Char"/>
        <w:basedOn w:val="DefaultParagraphFont"/>
        <w:link w:val="Title"/>
        <w:uiPriority w:val="10"/>
        <w:rPr>
            <w:rFonts w:ascii="黑体" w:eastAsia="黑体" w:hAnsi="黑体"/>
            <w:b/>
            <w:bCs/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:style>
</w:styles>'''
    }

    # 创建ZIP文件
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as docx:
        for file_path, content in docx_structure.items():
            docx.writestr(file_path, content.encode('utf-8'))

    return os.path.exists(filename)

def main():
    """创建模板文件"""
    templates = [
        ("基础模板.docx", "宋体", "适用于一般文档"),
        ("技术文档模板.docx", "Consolas/微软雅黑", "适用于技术文档"),
        ("商务文档模板.docx", "宋体/黑体", "适用于商务文档"),
    ]

    print("正在创建DOCX模板文件...")

    created_files = []
    for filename, description, usage in templates:
        try:
            if create_minimal_docx(filename):
                created_files.append(filename)
                print(f"✓ 已创建: {filename} - {usage}")
            else:
                print(f"✗ 创建失败: {filename}")
        except Exception as e:
            print(f"✗ 创建 {filename} 时出错: {e}")

    if created_files:
        print(f"\n🎉 成功创建 {len(created_files)} 个模板文件!")
        print("重启后端服务后即可在前端使用这些模板。")
        print("\n提示: 这些是基础模板，您可以在Word中打开并自定义样式。")
    else:
        print("\n❌ 没有成功创建任何模板文件")
        print("建议您手动在Word中创建模板文件")

if __name__ == "__main__":
    main()