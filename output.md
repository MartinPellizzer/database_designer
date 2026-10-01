| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 1      |
| Answer ID          | 1        |
| Stakeholder Role   | System Architect        |
| Question Text      | What exactly is the responsibility of the Relay Module within Aurora?    |
| Answer Text        | The Relay Module shall reliably and deterministically execute relay-output commands received from the CORE, provide the CORE with output status and module diagnostics, and transition its outputs to defined safe states when required by system-level fault conditions.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 2      |
| Answer ID          | 2        |
| Stakeholder Role   | System Architect        |
| Question Text      | Which functions of the overall Aurora system are allocated specifically to the Relay Module?    |
| Answer Text        | The Relay Module shall provide eight independently controlled relay-driver channels, manage their activation and deactivation, monitor relevant module/output faults, communicate their status and diagnostics to the CORE via Modbus RTU over RS-485, and enforce defined local fault-handling behavior.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 3      |
| Answer ID          | 3        |
| Stakeholder Role   | System Architect        |
| Question Text      | What behavior does the system require from each of the eight relay outputs?    |
| Answer Text        | Each output shall independently assume the ON or OFF state commanded by the CORE within the specified response time, while preventing an individual channel fault from affecting the other channels and maintaining the output's defined safe behavior under fault conditions.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 4      |
| Answer ID          | 4        |
| Stakeholder Role   | System Architect        |
| Question Text      | What must happen to every relay output when communication with the CORE is lost?    |
| Answer Text        | Upon detecting a communication timeout with the CORE, every relay output shall transition to its predefined safe state, which shall be OFF unless a system-level hazard analysis explicitly requires another state.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 5      |
| Answer ID          | 5        |
| Stakeholder Role   | System Architect        |
| Question Text      | What is the required system behavior if the Relay Module itself fails?    |
| Answer Text        | Any Relay Module failure that could compromise safe operation shall cause the affected outputs to transition to their defined safe states, prevent unintended activation, and provide sufficient fault information to the CORE to initiate the appropriate Aurora system fault response.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 6      |
| Answer ID          | 6        |
| Stakeholder Role   | CORE Firmware Engineer        |
| Question Text      | Which responsibilities belong to the CORE and which responsibilities belong to the Relay Module?    |
| Answer Text        | The CORE shall own all system-level decisions, sequencing, interlocks, operating modes and desired relay states, while the Relay Module shall execute those commands deterministically, manage its eight physical driver outputs, perform local hardware diagnostics, and report its status and faults to the CORE.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 7      |
| Answer ID          | 7        |
| Stakeholder Role   | CORE Firmware Engineer        |
| Question Text      | What commands must the CORE be able to send to the Relay Module?    |
| Answer Text        | The CORE shall be able to command each of the eight outputs independently, initialize and reset the module, request status and diagnostics, and synchronize or restore the required output states after startup or communication recovery.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 8      |
| Answer ID          | 8        |
| Stakeholder Role   | CORE Firmware Engineer        |
| Question Text      | What information must the Relay Module provide back to the CORE?    |
| Answer Text        | The Relay Module shall report the state of all eight outputs, module health, individual channel faults, communication status, relevant electrical/thermal diagnostics, firmware/hardware identification, and any condition preventing reliable output control.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 9      |
| Answer ID          | 9        |
| Stakeholder Role   | CORE Firmware Engineer        |
| Question Text      | How should the CORE detect that communication with the Relay Module has been lost?    |
| Answer Text        | The CORE shall use a supervised communication mechanism with a defined response timeout and consecutive failed transactions, declaring the Relay Module unavailable when the configured communication-loss threshold is exceeded.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 10      |
| Answer ID          | 10        |
| Stakeholder Role   | CORE Firmware Engineer        |
| Question Text      | What should the CORE do when communication with the Relay Module is lost?    |
| Answer Text        | The CORE shall immediately declare a Relay Module communication fault, prevent further normal relay commands, transition Aurora to the appropriate safe system state, notify the HMI, and automatically re-synchronize the required relay states only after reliable communication has been restored.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 11      |
| Answer ID          | 11        |
| Stakeholder Role   | Electrical Engineer        |
| Question Text      | What are the electrical specifications of the eight relay-driver outputs, based on the physical relays they must control?    |
| Answer Text        | Each driver shall independently and reliably energize its assigned relay coil across the full specified supply, temperature, and tolerance range, with adequate voltage/current margin, continuous-duty capability, short-circuit/overload protection, and no unintended activation during reset or fault conditions.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 12      |
| Answer ID          | 12        |
| Stakeholder Role   | Electrical Engineer        |
| Question Text      | What are the electrical characteristics of the physical relay coils connected to each of the eight driver outputs?    |
| Answer Text        | Each relay coil shall have a defined nominal voltage, allowable voltage range, nominal and maximum current, resistance/inductance, inrush behavior, continuous-duty rating, and release/operate characteristics that are fully compatible with its corresponding driver.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 13      |
| Answer ID          | 13        |
| Stakeholder Role   | Electrical Engineer        |
| Question Text      | What is the required input supply voltage range, including tolerances and transient conditions?    |
| Answer Text        | The module shall operate correctly over the complete specified nominal supply range, including component tolerances, steady-state variation, startup conditions, brownouts, overvoltage, ripple, and transient disturbances expected in the Aurora electrical cabinet.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 14      |
| Answer ID          | 14        |
| Stakeholder Role   | Electrical Engineer        |
| Question Text      | What protection is required to handle the inductive voltage transient generated when a relay coil is de-energized?    |
| Answer Text        | Each driver output shall incorporate appropriately sized suppression, such as a flyback diode or TVS/clamp network, to limit the coil-generated transient to a safe level without exceeding driver ratings or causing unacceptable relay release-time delays.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 15      |
| Answer ID          | 15        |
| Stakeholder Role   | Electrical Engineer        |
| Question Text      | What electrical behavior is required during power loss, brownout, and restoration of power?    |
| Answer Text        | During power loss or an out-of-range brownout, all relay outputs shall transition to and remain in their defined safe state without unintended activation, and after power restoration the module shall initialize deterministically with outputs disabled until valid control from the CORE is established.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 16      |
| Answer ID          | 16        |
| Stakeholder Role   | Safety Engineer        |
| Question Text      | What safety functions, if any, are assigned specifically to the Relay Module?    |
| Answer Text        | The Relay Module shall locally enforce the safety-related output constraints and fail-safe behavior defined for its eight relay channels, detect relevant hardware and output faults, and transition affected outputs to their predefined safe states independently of higher-level system decisions.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 17      |
| Answer ID          | 17        |
| Stakeholder Role   | Safety Engineer        |
| Question Text      | What is the required safe state for each of the eight relay outputs?    |
| Answer Text        | Each of the eight relay outputs shall have a formally defined safe state based on its associated hazard analysis, with OFF/de-energized as the default safe state unless a documented safety analysis requires a specific output to remain energized.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 18      |
| Answer ID          | 18        |
| Stakeholder Role   | Safety Engineer        |
| Question Text      | What shall happen to each relay output when the Relay Module detects an internal fault?    |
| Answer Text        | When the Relay Module detects an internal fault capable of compromising safe operation, it shall immediately prevent unsafe output activation, force all affected outputs to their defined safe states, latch or report the fault as required, and prevent reactivation until the fault-clear and reauthorization conditions are satisfied.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 19      |
| Answer ID          | 19        |
| Stakeholder Role   | Safety Engineer        |
| Question Text      | What shall happen to each relay output when communication with the CORE is lost?    |
| Answer Text        | When communication with the CORE is lost beyond the defined safety timeout, the Relay Module shall autonomously transition every output to its predefined safe state, maintain that state, report the communication fault when communication is restored, and require explicit reauthorization before returning to normal operation.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 20      |
| Answer ID          | 20        |
| Stakeholder Role   | Safety Engineer        |
| Question Text      | Which safety decisions must be made by the CORE, and which must be enforced locally by the Relay Module?    |
| Answer Text        | The CORE shall make all system-level safety decisions, operating-mode and shutdown decisions, while the Relay Module shall locally enforce output-level safety constraints, watchdog/communication-loss responses, internal fault handling, and the defined safe-state behavior without relying solely on the CORE.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 21      |
| Answer ID          | 21        |
| Stakeholder Role   | Process Engineer        |
| Question Text      | What process functions are controlled or influenced by the eight relay outputs of the Relay Module?    |
| Answer Text        | The eight relay outputs shall control or influence the ozone-generation process by operating the required process equipment and auxiliaries—such as ozone-generation power, cooling, gas/air or oxygen supply, valves, purge/ventilation, and other process actuators—according to the defined process sequence and interlocks.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 22      |
| Answer ID          | 22        |
| Stakeholder Role   | Process Engineer        |
| Question Text      | What is the required sequence of operations for starting ozone generation?    |
| Answer Text        | The startup sequence shall verify all required permissives, establish the required gas flow and supporting utilities, enable cooling and other auxiliaries, confirm their healthy operating feedback, energize the ozone-generation system, and only then transition Aurora to the normal ozone-production state.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 23      |
| Answer ID          | 23        |
| Stakeholder Role   | Process Engineer        |
| Question Text      | What is the required sequence of operations for stopping ozone generation?    |
| Answer Text        | The shutdown sequence shall first disable ozone generation, maintain the required cooling and gas-flow/purge functions for the specified post-run period, safely de-energize the remaining auxiliaries in the defined order, and finally confirm that the process has reached the stopped state.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 24      |
| Answer ID          | 24        |
| Stakeholder Role   | Process Engineer        |
| Question Text      | What conditions must be satisfied before ozone generation is permitted to start?    |
| Answer Text        | Ozone generation shall be permitted only when all required utilities are available, gas flow and cooling are within their specified limits, required valves and auxiliaries are in their correct states, no active safety or process interlock is violated, all required feedback signals are valid, and the system is in an authorized operating mode.      |

| Field              | Value                      |
| ------------------ | -------------------------- |
| Question ID        | 25      |
| Answer ID          | 25        |
| Stakeholder Role   | Process Engineer        |
| Question Text      | What process conditions require ozone generation to stop immediately?    |
| Answer Text        | Ozone generation shall stop immediately whenever a condition capable of creating an unsafe or uncontrolled process state is detected, including loss of required gas flow or cooling, critical equipment failure, hazardous process-variable limits, loss of required safety permissives, emergency shutdown, or any other defined critical interlock.      |

