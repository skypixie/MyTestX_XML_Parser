from PyQt5.QtWidgets import QApplication, QFileDialog
from xml.etree import ElementTree
import sys
import os


def parse(filename):
    result = {}
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    save_filename = QFileDialog.getSaveFileName(None, "Сохранить файл",
                                                os.curdir, "Text (*.txt)")[0]
    
    for task in root.find("Groups").find("Group").find("Tasks"):
        q_text = task.find("QuestionText").find("PlainText").text
        answers = []
        try:
            for variant in task.find("Variants").findall("VariantText"):
                if variant.attrib["CorrectAnswer"] == "True":
                    answers.append(variant.find("PlainText").text)
        except Exception:
            answers.append(task.find("InputText").find("Value").text)
        result[q_text] = answers
    
    print(save_filename)
    with open(save_filename, "w") as file:
        for question in result:
            file.write(f"{question}\n")
            for ans in result[question]:
                file.write(f"-{ans}\n")
            file.write("\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    open_filename = QFileDialog.getOpenFileName(None, "Открыть файл",
                                                os.curdir, "XML files (*.xml)")[0]
    parse(open_filename)
    app.quit()
