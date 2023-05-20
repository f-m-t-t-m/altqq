import org.example.GaussLinearEquationSolverPivot;
import org.example.GaussLinearEquationSolverStrokePivot;
import org.junit.jupiter.api.Test;

import java.awt.*;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class GaussLinearEquationPivotTest {

    double[][] a = {{2, 1, -1},
                    {-3, -1, 2},
                    {-2, 1, 2}};
    double[] b = {8, -11, -3};
    double[] expected = {2, 3, -1};

    @Test
    void test_get_pivot() {
        GaussLinearEquationSolverPivot solver = new GaussLinearEquationSolverPivot();
        GaussLinearEquationSolverPivot.Point actual = solver.findPivot(a, 0, 0);
        assertEquals(1, actual.getX());
        assertEquals(0, actual.getY());
    }

    @Test
    void test_pivot() {
        GaussLinearEquationSolverPivot solver = new GaussLinearEquationSolverPivot();
        double[] actual = solver.solve(a, b);
        for (int i = 0; i < actual.length; ++i) {
            actual[i] = Math.round(actual[i] * 1e6) / 1e6;
        }
        assertArrayEquals(expected, actual);
    }


}
