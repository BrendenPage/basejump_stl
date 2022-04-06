
from __future__ import print_function
import sys

num_rows_p = int(sys.argv[1])
num_cols_p = int(sys.argv[2])
num_dly_p  = int(sys.argv[3])

num_els_p = num_rows_p*num_cols_p

print("""
// ## AUTOGENERATED; DO NOT MODIFY
// ## num_rows_p = {num_rows_p}
// ## num_cols_p = {num_cols_p}
// ## num_dly_p = {num_dly_p}
""".format(num_rows_p=num_rows_p, num_cols_p=num_cols_p, num_dly_p=num_dly_p))

print("""
module bsg_rp_clk_gen_osc_v3_row
 (input    async_reset_neg_i
  , input  async_set_neg_i
  , input  clkgate_i
  , input  clkdly_i
  , input  clkfb_i
  , input  ctl_i
  , output clk_o
  );

  wire ctl_r;
  DFCSNQD1BWP7T30P140ULVT D0 (.Q(ctl_r), .CP(clkgate_i), .D(ctl_i), .CDN(async_reset_neg_i), .SDN(async_set_neg_i));

  wire ctl_en;
  CKND2D1BWP7T30P140ULVT N0 (.ZN(ctl_en), .A1(clkdly_i), .A2(ctl_r));

  wire hibit;
  TIEHBWP7T30P140ULVT T0 (.Z(hibit));
  wire lobit;
  TIELBWP7T30P140ULVT T1 (.ZN(lobit));

  wire fb;
  CKND2D1BWP7T30P140ULVT N1 (.ZN(fb), .A1(clkfb_i), .A2(hibit));
  CKND2D1BWP7T30P140ULVT N2 (.ZN(clk_o), .A1(fb), .A2(ctl_en));

endmodule
""")

print("""
module bsg_rp_clk_gen_osc_v3_col
  (input async_reset_i
   , input clkgate_i
   , input clkdly_i
   , input clkfb_i
   , input [{num_rows_p}-1:0] ctl_one_hot_i
   , output clk_o
   );

  wire hibit;
  TIEHBWP7T30P140ULVT T0 (.Z(hibit));
  wire lobit;
  TIELBWP7T30P140ULVT T1 (.ZN(lobit));

  wire clkgate_inv;
  CKND1BWP7T30P140ULVT I0 (.ZN(clkgate_inv), .I(clkgate_i));

  wire clkdly_inv;
  CKND1BWP7T30P140ULVT I1 (.ZN(clkdly_inv), .I(clkdly_i));

  wire async_reset_neg;
  INVD1BWP7T30P140ULVT I2 (.ZN(async_reset_neg), .I(async_reset_i));

  wire [{num_rows_p}:0] clkfb;
  assign clkfb[0] = clkfb_i;

  wire [{num_rows_p}-1:0] async_reset_neg_li, async_set_neg_li;
""".format(num_rows_p=num_rows_p))

for i in range(0, num_rows_p):
  if i == 0:
    print("""
      assign async_reset_neg_li[{i}] = hibit;
      assign async_set_neg_li[{i}]   = async_reset_neg;
    """.format(i=i))
  else:
    print("""
      assign async_reset_neg_li[{i}] = async_reset_neg;
      assign async_set_neg_li[{i}]   = hibit;
    """.format(i=i))

  print("""
      bsg_rp_clk_gen_osc_v3_row row_{i}_BSG_DONT_TOUCH
        (.async_reset_neg_i(async_reset_neg_li[{i}])
         ,.async_set_neg_i(async_set_neg_li[{i}])
         ,.clkgate_i(clkgate_inv)
         ,.clkdly_i(clkdly_inv)
         ,.clkfb_i(clkfb[{i}])
         ,.ctl_i(ctl_one_hot_i[{i}])
         ,.clk_o(clkfb[{ip1}])
         );
""".format(i=i, ip1=i+1))

print("""
  assign clk_o = clkfb[{num_rows_p}];

endmodule
""".format(num_rows_p=num_rows_p))

