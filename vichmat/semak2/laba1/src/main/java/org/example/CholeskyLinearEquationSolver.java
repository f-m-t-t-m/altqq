package org.example;

public class CholeskyLinearEquationSolver extends LULinearEquationSolver {

    @Override
    public double[] solve(double[][] a, double[] b) {
        CholeskyDecomposition cDecomposition = CholeskyDecomposition.from(a);
        double[] Y = getY(cDecomposition.getT_transposed(), b);
        return backwardStep(cDecomposition.getT(), Y);
    }
}
