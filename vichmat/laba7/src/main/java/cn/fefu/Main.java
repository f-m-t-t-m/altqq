package cn.fefu;

import com.github.sh0nk.matplotlib4j.Plot;
import com.github.sh0nk.matplotlib4j.PythonExecutionException;
import org.apache.commons.math3.analysis.differentiation.DerivativeStructure;

import java.io.IOException;
import java.util.ArrayList;
public class Main {

    static double a = 0.4;
    static double b = 0.9;

    private class myFunc {
        private final double a;
        private final double b;
        private final double x_;

        public double apply(double x) {
            return funcDerivative(x_, 0) + funcDerivative(x_, 1)*(x- x_) + a*Math.pow(x-x_, 2)/2 +
                    b*Math.pow(x-x_, 3)/6;
        }
        public myFunc(double a, double b, double x_) {
            this.a = a;
            this.b = b;
            this.x_ = x_;
        }

        public double getA() {
            return this.a;
        }
    }

    public static ArrayList<Double> getGrid(double a, double b, int N) {
        ArrayList<Double> grid = new ArrayList<>();
        double h = (b - a) / N;
        for(int i = 0; i <= N; i++) {
            grid.add(a + i * h);
        }

        return grid;
    }

    private static double funcDerivative(double x, int order) {
        DerivativeStructure x_ = new DerivativeStructure(1, order+1, 0, x);
        DerivativeStructure res = (x_.pow(2)).add(x_.log());
        return res.getPartialDerivative(order);
    }

    private static double[] solve(double[][] A, double[] B) {
        int len = B.length;
        double[] x = new double[len];
        double[] alpha = new double[len-1];
        double[] beta = new double[len-1];

        alpha[0] = -A[0][1] / A[0][0];
        beta[0] = B[0] / A[0][0];
        for(int i = 1; i < len - 1; ++i) {
            alpha[i] = -A[i][i+1] / (A[i][i] + A[i][i-1] * alpha[i-1]);
            beta[i] = (B[i] - A[i][i-1] * beta[i-1]) / (A[i][i] + A[i][i-1] * alpha[i-1]);
        }
        x[len-1] = (B[len-1] - A[len-1][len-2] * beta[len-2]) / (A[len-1][len-1] + A[len-1][len-2] * alpha[len-2]);

        for(int i = len - 1; i > 0; --i) {
            x[i-1] = x[i] * alpha[i-1] + beta[i-1];
        }

        return x;
    }

    public static void main(String[] args) throws PythonExecutionException, IOException {
        ArrayList<Double> grid = getGrid(a, b, 10);
        double m0 = funcDerivative(a, 1);
        double mn = funcDerivative(b, 1);
        double[][] A = new double[grid.size()][grid.size()];
        double[] B = new double[grid.size()];
        A[0][0] = 1;
        B[0] = m0;
        for(int i = 0; i < grid.size()-2; ++i) {
            A[i+1][i] = 1;
            A[i+1][i+1] = 4;
            A[i+1][i+2] = 1;
            B[i+1] = (funcDerivative(grid.get(i+2), 0) - funcDerivative(grid.get(i), 0)) * 60;
        }
        A[grid.size()-1][grid.size()-1] = 1;
        B[grid.size()-1] = mn;
        double[] m = solve(A, B);

        double[] a_ = new double[grid.size()];
        double[] b_ = new double[grid.size()];
        for(int i = 0; i < grid.size()-1; ++i) {
            a_[i] = 6/0.05 * ((funcDerivative(grid.get(i+1), 0) - funcDerivative(grid.get(i), 0))/0.05
                    - (m[i+1]+2*m[i])/3);
            b_[i] = 12/Math.pow(0.05, 2) * ((m[i+1] + m[i])/2 - (funcDerivative(grid.get(i+1), 0)
                    - funcDerivative(grid.get(i), 0))/0.05);
        }

        myFunc[] func = new myFunc[grid.size()];
        for(int i = 0; i < grid.size(); ++i) {
            func[i] = new Main().new myFunc(a_[i], b_[i], grid.get(i));
        }

        ArrayList<Double> S = new ArrayList<>();
        ArrayList<Double>  f = new ArrayList<>();
        ArrayList<Double>  xs = new ArrayList<>();

        for(int i = 0; i < grid.size()-1; ++i) {
            double x = grid.get(i);
            myFunc funcToCalculate = func[i];
            for(double j = x; j < grid.get(i+1); j += 0.01) {
                xs.add(j);
                S.add(funcToCalculate.apply(j));
                f.add(funcDerivative(j, 0));
            }
        }
        Plot plt = Plot.create();
        plt.plot().add(xs, S).label("Кубический сплайн").linewidth(1.);
        plt.plot().add(xs, f).label("График функции").linewidth(1.);
        plt.legend();
        plt.show();
        plt.savefig("fig1.svg");
        plt.executeSilently();
    }
}