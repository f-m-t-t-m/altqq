package org.example;

public class CholeskyDecomposition {

    private double[][] T;
    private double[][] T_transposed;

    private void decompose(double[][] a) {
        init(a.length);
        for (int i = 0; i < a.length; ++i) {
            for (int j = i; j < a.length; ++j) {
                if (i == j) {
                    T[i][j] = Math.sqrt(a[i][j] - calculateSum(i, j, i));
                } else {
                    T[i][j] = (a[i][j] - calculateSum(i, j, i))/T[i][i];
                }
            }
        }
        T_transposed = MatrixUtils.transpose(T);
    }

    private void init(int n) {
        T = new double[n][n];
    }

    private double calculateSum(int i, int j, int to) {
        double res = 0.;
        for (int k = 0; k < to; ++k) {
            res += T[k][i] * T[k][j];
        }
        return res;
    }

    public static CholeskyDecomposition from(double[][] a) {
        CholeskyDecomposition kd = new CholeskyDecomposition();
        kd.decompose(a);
        return kd;
    }

    public double[][] getT() {
        return T;
    }

    public double[][] getT_transposed() {
        return T_transposed;
    }

    private CholeskyDecomposition() {
    }
}
