# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.types import Logic

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Test counter ability
    dut.ui_in.value = 0
    dut.uio_in.value = 0b10 # enable output, no load

    for i in range(256):
        # Wait for one clock cycle to see the output values
        await ClockCycles(dut.clk, 1)

        # The following assersion is just an example of how to check the output values.
        # Change it to match the actual expected output of your module:
        assert dut.uo_out.value == i

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
    dut._log.info("Counter passed all 256 units")
    # check for high impedance, then check load, and then reset
    dut._log.info("Testing High impedance state")
    dut.uio_in.value = 0b00
    dut.ui_in.value = 8
    await ClockCycles(dut.clk, 1)
    assert str(dut.uo_out.value) == 'ZZZZZZZZ' or dut.uo_out.value == 0, "Output was not high impedance"
    dut.uio_in.value = 0b10
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0b11
    assert dut.uo_out.value == 1, "Value did not wrap around"
    await ClockCycles(dut.clk, 2) # Counter needs 2 cycles to take on load values
    dut._log.info("Testing load enable")
    assert dut.uo_out.value == 8, (f"Output was not set by load value: {dut.uo_out.value}") 
    dut.uio_in.value = 0b10
    await ClockCycles(dut.clk, 2) # Counter needs 2 cycles to take on load values
    dut._log.info("Testing counter after load enable")
    for i in range(9, 12):
        assert dut.uo_out.value == i, "Counter did not resume after loading"
        await ClockCycles(dut.clk, 1)
    dut._log.info("Testing reset hold")
    dut.rst_n.value = 0 
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 0
    dut.rst_n.value = 1 
    await ClockCycles(dut.clk, 1)
    dut._log.info("Testing load hold")
    dut.uio_in.value = 0b11
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 8
    