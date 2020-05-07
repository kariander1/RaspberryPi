import deviceManager

ld = deviceManager.init_led(27)
motion_d =deviceManager.init_motion_detector(23)
motion_d.add_trigger_pin(27)
motion_d.start_listening()

text = input()

deviceManager.exit_program()