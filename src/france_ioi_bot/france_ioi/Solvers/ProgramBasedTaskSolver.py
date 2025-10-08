from typing import Tuple
import os
import re
import unicodedata
from bs4 import BeautifulSoup
from france_ioi.Account import Account
from france_ioi.Task import Task, TaskCategory

def remove_accents(text: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_name(name: str) -> str:
    name = remove_accents(name)
    name = re.sub(r'\s+', '_', name)
    return name

def solve_program_based_task(account: Account, task: Task) -> Tuple[bool, bool]:
    assert task.category == TaskCategory.VALIDATION or task.category == TaskCategory.CHALLENGE or task.category == TaskCategory.DISCOVERY or task.category == TaskCategory.APPLICATION
    answerFile = re.sub(r'[:"]', '', f"./answers/{clean_name(task.parent.parent.title)}/{clean_name(task.parent.title)}/{clean_name(task.title)}.py")
    if not os.path.isfile(answerFile):
        print(f":: No answer file found for task at '{answerFile}' ({task.link})")
        return False, False
    with open(answerFile, 'r', encoding='utf-8') as f:
        fileContents = f.read()

    queryParamsMatch = re.search(r'idChapter=\d+&idTask=\d+', task.link)
    assert queryParamsMatch is not None

    queryParams = queryParamsMatch.group(0)
    response = account.postHttpQueryAuthed(f"/algo/evaluation.php?{queryParams}&bEvaluate=1&sOnlyBlock=mainContent", {
        "bNoSave": "0",
        "sSourceContents": fileContents,
        "sExtension": 'Python'
    })

    if response is None:
        return False, True

    responseContents = response.content.decode()
    doc = BeautifulSoup(responseContents, "html.parser")

    if "Félicitations" in responseContents:
        print(f":: Successfully solved program-based task '{task.title}'!")
        return True, True

    if "La réponse donnée par votre programme est incorrecte." in responseContents:
        print(f":: The program for task '{task.title}' was executed successfully, but the answer is incorrect.")
        return False, True

    if "Erreur d'exécution." not in responseContents:
        print(f":: The program for task '{task.title}' seems to not have been accepted, retrying in 5 seconds...")
        return solve_program_based_task(account, task)

    tr = doc.find("tr", { "class": "evaluation-result-error" })
    assert tr is not None

    programError = doc.find("pre")
    assert programError is not None

    print(f":: The program for task '{task.title}' failed to execute! Here is the error message:\n{programError.get_text()}")
    return False, True