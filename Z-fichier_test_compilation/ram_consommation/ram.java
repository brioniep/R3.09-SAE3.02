import java.util.ArrayList;

public class ram {
    public static void main(String[] args) {
        ArrayList<byte[]> memory = new ArrayList<>();
        try {
            for (int i = 0; i < 600; i++) {
                memory.add(new byte[1024 * 1024]); // Allocate 1MB
            }
            System.out.println("Consumed 600MB of memory");
            Thread.sleep(60000); // Sleep for 1 minute
        } catch (InterruptedException e) {
            System.err.println("Program interrupted");
        }
    }
}