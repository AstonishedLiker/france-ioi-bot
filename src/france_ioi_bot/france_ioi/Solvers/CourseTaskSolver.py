import re
from france_ioi.Account import Account
from france_ioi.Task import Task, TaskCategory

def solve_course_task(account: Account, task: Task) -> bool:
    assert task.category == TaskCategory.COURSE

    queryParamsMatch = re.search(r'idChapter=\d+&idCourse=\d+', task.link)
    assert queryParamsMatch is not None

    queryParams = queryParamsMatch.group(0)
    response = account.postHttpQueryAuthed(f'/algo/evaluation.php?{queryParams}&bEvaluate=1&sOnlyBlock=mainContent', {
        "bRead": "Marquer+comme+lu+et+continuer"
    })

    if response is None:
        return False

    return True