import org.opensourcephysics.controls.*;
import org.opensourcephysics.frames.*;

public class FreewayAppRamp extends AbstractSimulation {

    FreewayRamp freeway = new FreewayRamp ();
    DisplayFrame display = new DisplayFrame ("Freeway");
    LatticeFrame spaceTime = new LatticeFrame ("space", "time", "Space Time Diagram");

    public FreewayAppRamp () {
        display.addDrawable(freeway) ;
    }

    public void initialize () {
        freeway.numberOfCars = control.getInt("Number of cars");
        freeway.roadLength = control.getInt("Road length");
        freeway.p = control.getDouble("Slow down probability");
        freeway.p2 = control.getDouble("Exiting ramp probability");
        freeway.maximumVelocity = control.getInt("Maximum velocity");
        display.setPreferredMinMax(0, freeway.roadLength, -3, 4);
        freeway.initialize(spaceTime);
    }

    public void doStep () {
        freeway.step();
    }

    public void reset () {
        control.setValue("Number of cars", 10);
        control.setValue("Road length", 50);
        control.setValue("Slow down probability" , 0.5);
        control.setValue("Exiting ramp probability" , 0.5);
        control.setValue("Maximum velocity" , 2 );
        control.setValue("Steps between plots" , 1);
        enableStepsPerDisplay(true);
    }

    public void resetAverages () {
        freeway.flow = 0;
        freeway.steps = 0;
    }

    public static void main (String [] args) {
        SimulationControl control =
        SimulationControl.createApp (new FreewayAppRamp());
        control.addButton("resetAverages", "resetAverages");
    }
}
