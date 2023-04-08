package org.example;

public class LUDecomposition {

    private double[][] L;
    private double[][] U;

    private void decompose(double[][] a) {
        init(a.length);
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < a.length; ++j) {
                if (i <= j) {
                    U[i][j] = a[i][j] - calculateSum(i, j, i);
                }
                if (i > j) {
                    L[i][j] = (a[i][j] - calculateSum(i, j, j))/U[j][j];
                }
            }
        }
    }

    private void init(int n) {
        L = new double[n][n];
        for (int i = 0; i < n; i++) {
            L[i][i] = 1;
        }
        U = new double[n][n];
    }

    private double calculateSum(int i, int j, int to) {
        double res = 0.;
        for (int k = 0; k < to; ++k) {
            res += L[i][k]*U[k][j];
        }
        return res;
    }

    public double[][] getL() {
        return L;
    }

    public double[][] getU() {
        return U;
    }

    public LUDecomposition(double[][] a) {
        decompose(a);
    }

}
