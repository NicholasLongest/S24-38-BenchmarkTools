/* Quartus Prime Version 22.1std.0 Build 915 10/25/2022 SC Lite Edition */
JedecChain;
	FileRevision(JESD32A);
	DefaultMfr(6E);

	P ActionCode(Ign)
		Device PartName(5CSEMA5F31) MfrSpec(OpMask(0) FullPath("/fpu_70.sof"));
	P ActionCode(Cfg)
		Device PartName(5CSEMA5F31) Path("/") File("fpu_70.sof") MfrSpec(OpMask(1));

ChainEnd;

AlteraBegin;
	ChainType(JTAG);
AlteraEnd;
