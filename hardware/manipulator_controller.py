class ManipulatorController:
    def __init__(self):
        self.joint_targets = [0.0, 0.0, 0.0, 0.0]
        self.gripper_state = 0.0

    def set_joint_positions(self, joints, duration=2.0):
        self.joint_targets = joints

    def open_gripper(self):
        self.gripper_state = -0.8

    def close_gripper(self):
        self.gripper_state = 0.2

    def remove_obstacle(self):
        self.close_gripper()
        self.set_joint_positions([0.0, -0.5, 0.4, 0.0])
        self.open_gripper()
