RandomUnitriangular := function(dimension, F, offset)
# Generate a random unitriangular matrix of size n by n in the (finite) field F.
# The offset variable encodes the number of diagonals above the main diagonal that we keep to be zero.
	local M, i, j;
	# Initialise a zero matrix.
	M := [ ];
	for i in [1..n] do
		Append(M, [ListWithIdenticalEntries(n, Zero(F))]);
	od;
	# Insert the identity and the random diagonals.
	for i in [1..n] do
		M[i][i] := Identity(F);
		for j in [i+1+offset..n] do
			M[i][j] := Random(F);
		od;
	od;
	return M;
end;

RandomPGroupModule := function(n, F, offset, number_of_generators)
# Generate a random faithful n-dimensional modular representation of a random p-group.
# Methodology: Simply generate a random subgroup of the group of unitriangular matrices (which is the Sylow p-subgroup of GL_n(F)) by randomly choosing some generators.
# The offset is used in the random generation of the unitriangular matrices; increasing the offset will make the expected size of the p-group smaller.
	local M, generators, i;
	generators := [ ];
	for i in [1..number_of_generators] do
		M := RandomUnitriangular(n, F, offset);
		Append(generators, [M]);
	od;
	return GModuleByMats(generators, F);
end;

TestConjecture := function(n, F, offset, number_of_generators, iterations)
# Benson's conjecture concerns itself with possible constrains on the dimensions of the indecomposable summands of End(M) when M is a finite-dimensional p-group representation. For instance, when p = 2, it is conjectured that, if M is odd-dimensional indecomposable, then the indecomposable summands of End(M) will, with the exception of the unique trivial summand, all have dimension divisible by 4.
# This function repeatedly (N times where N = 'iterations') generates n-dimensional p-group representations, decomposes it, and evaluates the dimensions of the endomorphism group of these indecomposable summands.
	local i, M, summand, dim, outcomes, out;
	for i in [1..iterations] do
		M := RandomPGroupModule(n, F, offset, number_of_generators);
		for summand in MTX.Indecomposition(M) do
			dim := Length(summand[1]);
			# Depending on your intentions you may want to add some restrictions to this if-statement. At p = 2, the conjecture concerns itself with odd-dimensional representations, so you may want to add 'and dim mod 2 = 1' to filter out some irrelevant stuff.
			if dim > 1 then
			#if dim > 1 and dim % 2 = 1 then
				Print("dim(M) = ");
				Print(dim);
				Print("; End(M) splits up as ");
				outcomes := MTX.Indecomposition(TensorProductGModule(summand[2], DualGModule(summand[2])));
				for out in outcomes do
					Print(Length(out[1]));
					Print(" ");
				od;
				Print("\n");
			fi;
		od;
	od;
end;
