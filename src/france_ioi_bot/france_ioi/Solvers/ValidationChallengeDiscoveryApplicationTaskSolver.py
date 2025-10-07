import os
import re
from bs4 import BeautifulSoup
from france_ioi.Account import Account
from france_ioi.Task import Task, TaskCategory

def solve_validation_challenge_discovery_application_task(account: Account, task: Task) -> bool:
    assert task.category == TaskCategory.VALIDATION or task.category == TaskCategory.CHALLENGE or task.category == TaskCategory.DISCOVERY or task.category == TaskCategory.APPLICATION
    # we remove any NTFS disallowed caracters from the filename
    answerFile = re.sub(r'[<>:"\\|?*]', '', f"./answers/{task.parent.parent.title}/{task.parent.title}/{task.title}.py")
    if not os.path.isfile(answerFile):
        print(f":: No answer file found for task {task.title} at '{answerFile}'")
        return False
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
        return False

    responseContents = response.content.decode()
    doc = BeautifulSoup(responseContents, "html.parser")

    if "Félicitations" in responseContents:
        return True

    if "La réponse donnée par votre programme est incorrecte." in responseContents:
        print(f":: The program for task {task.title} was executed successfully, but the answer is incorrect.")
        return False

    if "Erreur d'exécution." not in responseContents:
        print(f":: The program for task {task.title} seems to not have been accepted.")
        return False

    tr = doc.find("tr", { "class": "evaluation-result-error" })
    assert tr is not None

    programError = doc.find("pre")
    assert programError is not None

    print(f":: The program for task {task.title} failed to execute! Here is the error message:\n{programError.get_text()}")
    return False