from random import shuffle
from typing import List

import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task
from rlbench.const import colors

CUPS_NAMES = ["cup1", "cup2", "cup3"]

class StackCups(Task):
    def init_task(self) -> None:
        success_sensor = ProximitySensor("success")
        self.cup1 = Shape("cup1")
        self.cup2 = Shape("cup2")
        self.cup3 = Shape("cup3")
        self.cup1_visual = Shape("cup1_visual")
        self.cup2_visual = Shape("cup2_visual")
        self.cup3_visaul = Shape("cup3_visual")

        self._cups = [Shape(name) for name in CUPS_NAMES]
        self._table = Shape("diningTable")
        self._init_relpose_cup_to_table = {name: cup.get_pose(relative_to=self._table) for cup, name in zip(self._cups, CUPS_NAMES)}

        self.register_graspable_objects([self.cup1, self.cup2, self.cup3])
        self.register_success_conditions(
            [
                DetectedCondition(self.cup1, success_sensor),
                DetectedCondition(self.cup3, success_sensor),
                NothingGrasped(self.robot.gripper),
            ]
        )

    def init_episode(self, index: int) -> List[str]:
        shuffle(self._cups)
        for name, cup in zip(CUPS_NAMES, self._cups):
            cup.set_pose(self._init_relpose_cup_to_table[name], relative_to=self._table)

        self.variation_index = index
        target_color_name, target_rgb = colors[index]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        other1_color_name, other1_rgb = colors[random_idx]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        other2_color_name, other2_rgb = colors[random_idx]

        self.cup2_visual.set_color(target_rgb)
        self.cup1_visual.set_color(other1_rgb)
        self.cup3_visaul.set_color(other2_rgb)

        return [
            f'stack the {other1_color_name} cup and the {other2_color_name} cup on top of the {target_color_name} cup',
            "stack the other cups on top of the %s cup" % target_color_name,
            "place two of the cups onto the odd cup out",
            "put the remaining two cups on top of the %s cup"
            % target_color_name,
            "pick up and set the cups down into the %s cup" % target_color_name,
            "create a stack of cups with the %s cup as its base"
            % target_color_name,
            "keeping the %s cup on the table, stack the other two onto it"
            % target_color_name,
        ]

    def variation_count(self) -> int:
        return len(colors)
