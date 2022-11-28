package cn.fefu;

public class Main {
    private static Double func(Double x) {
        return Math.pow(x, 2) + Math.log(x);
    }

    private static Double getH(double[] interval, int N) {
        return (interval[1] - interval[0]) / N;
    }

    private static Double leftRectangles(double[] interval, int n) {
        double res = 0.;
        double h = getH(interval, n);
        double currentX = interval[0];
        while ( currentX < interval[1] ) {
            res += func(currentX) * h;
            currentX += h;
        }
        return res;
    }

    public static void main(String[] args) {
        double[] interval = {0.4, 0.9};
        double eps = 10E-6;
        int N = 10;
        while( Math.abs(leftRectangles(interval, N) - leftRectangles(interval, 2*N)) > eps ) {
            N *= 2;
        }
        System.out.printf("N = %d\nCalculated integral value = %f", N, leftRectangles(interval, N));
    }
}