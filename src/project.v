/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_eight_bit_counter ( // define all your ports
  input wire [7:0] ui_in,    // Load inputs
  output wire [7:0] uo_out,   // Tri state outputs
  
  input  wire [7:0] uio_in,   // IOs: Input path
  output wire [7:0] uio_out,  // IOs: Output path
  output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)

  input wire ena,      // always 1 when the design is powered, so you can ignore it
  input wire clk,      // clock
  input wire rst_n     // reset_n - low to reset
);
  reg [7:0] count; // internal variable/state
  wire ld = uio_in[0];
  wire en_out = uio_in[1]; // for making output high impedance

  // List all unused inputs to prevent warnings
  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out = 8'h00;
  assign uio_oe  = 8'h00;

  // always @(*) ... PROCEDURAL COMBINATIONAL, equivalent to continuous (assign) as 
  // behavior is determined when any dependent signal is changed. Better for larger if/else ladders

  always @(posedge clk or negedge rst_n) begin // SEQUENTIAL, behavior that is defined on a clock signal
    
    if (!rst_n) begin
      count <= 8'h00;
    end else if (ld) begin
      count <= ui_in;
    end else begin
      count <= count + 1; // will naturally wrap from 255 to 0
    end
  end
  

  assign uo_out = en_out ? count : 8'hzz; // if not enabled, high impedance

  
  //wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule

