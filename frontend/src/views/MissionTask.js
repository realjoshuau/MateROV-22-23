import React, { useState } from 'react';

function MissionTask(props){
    const { missionTasks, setMissionTasks, pilotOrCopilot } = props;
    // var pilotOrCopilot = "copilot";
    // var missionTaskInit = ["task1", "task2", "task3"];
    const isCoPilot = pilotOrCopilot === "copilot";
    // const [missionTasks, setMissionTasks] = useState(missionTaskInit);

    return (
        <div>
            <h1>Mission Tasks</h1>
            <ul>
                {missionTasks.map((task, index) => {
                        return (
                            <li key={index}>
                                {task.checked ? <s>{task.task}</s> : task.task}
                                <br />
                                { task.checked ? <button onClick={() => {
                                    const newTasks = [...missionTasks];
                                    newTasks[index].checked = false;
                                    setMissionTasks(newTasks);
                                } }>Uncheck</button> : <button onClick={() => {
                                    const newTasks = [...missionTasks];
                                    newTasks[index].checked = true;
                                    setMissionTasks(newTasks);
                                } }>Check</button> }
                                { isCoPilot && <button onClick={() => {
                                    const newTasks = [...missionTasks];
                                    newTasks.splice(index, 1);
                                    setMissionTasks(newTasks);
                                } }>Remove</button> }
                            </li>
                        )
                })}
            </ul>
            {isCoPilot && <button onClick={() => {
                setMissionTasks([...missionTasks, {
                    task: prompt("Enter task: "),
                    checked: false
                }]);
            }
            }>Add Task</button>}
        </div>
    )
}

export default MissionTask;