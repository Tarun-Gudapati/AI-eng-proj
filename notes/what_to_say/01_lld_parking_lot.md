# What to say 1: the LLD method, and a parking lot

Goal: if an interviewer says "design a parking lot" tomorrow, you can talk for 30 minutes and
sketch the classes. Read it once, then say each section out loud without looking.

---

## The LLD method (use it for every LLD question: library, parking lot, elevator, ATM)

1. **Clarify the requirements (3 to 5 minutes).** Ask before you draw. Write down 4 to 6
   features and what is out of scope.
2. **Find the entities.** The nouns in the requirements become classes.
3. **Relationships.** "Has a" (composition), "is a" (inheritance), "uses" (dependency).
   Say how many: one floor has many spots.
4. **Classes, with fields and the key methods.** Only the methods the requirements need.
5. **Patterns and SOLID.** Name a pattern only where it solves a real problem, and say which one.
6. **Edge cases and concurrency.** What happens when two things happen at the same time?
7. **Extensions.** "If you wanted EV charging, what changes?" Show that your design bends.

Interviewers grade the **order** and the **questions you ask**, not only the final diagram.

---

## Step 1: questions to ask

- How many floors? Several entrances and exits?
- Which vehicle types? (Motorbike, car, truck.) Which spot sizes? (Small, compact, large.)
- Can a small vehicle use a bigger spot? (Usually yes: a bike can use a car spot.)
- How is the price worked out? Hourly? Different for each vehicle type?
- How do people pay? Cash, card, UPI? At the exit, or at a kiosk?
- Do we show free spots per floor on a display board?

Then say your scope: "Multi-floor, three vehicle types, ticket at entry, pay at exit, hourly
price by vehicle type. Out of scope: reservations, monthly passes."

## Step 2: entities

`ParkingLot`, `Floor`, `ParkingSpot`, `Vehicle`, `Ticket`, `EntryGate`, `ExitGate`,
`Payment`, `PricingStrategy`, `SpotAllocationStrategy`, `DisplayBoard`.

## Step 3: relationships

- A `ParkingLot` **has** many `Floor`s and many gates (composition: no floor without the lot).
- A `Floor` **has** many `ParkingSpot`s.
- `Car`, `Bike` and `Truck` **are** `Vehicle`s (inheritance), or one `Vehicle` with a `VehicleType` enum.
- A `Ticket` **references** a `Vehicle` and a `ParkingSpot`, plus the entry time.
- `ExitGate` **uses** a `PricingStrategy` and a `Payment`.

Say the trade-off for vehicles: subclasses only pay off if the types *behave* differently. If
only the size differs, an enum is simpler. Saying this out loud scores points.

## Step 4: the classes (C#, signatures only)

```csharp
enum VehicleType { Bike, Car, Truck }
enum SpotSize { Small, Compact, Large }
enum TicketStatus { Active, Paid, Lost }

class Vehicle { string Plate; VehicleType Type; }

class ParkingSpot {
    int Id; SpotSize Size; bool IsFree; Vehicle? Current;
    bool CanFit(Vehicle v);          // bike fits Small or larger, car Compact or larger, truck Large
    void Park(Vehicle v); void Leave();
}

class Floor { int Number; List<ParkingSpot> Spots; int FreeCount(SpotSize size); }

class Ticket { Guid Id; Vehicle Vehicle; ParkingSpot Spot; DateTime EntryTime; TicketStatus Status; }

interface IPricingStrategy { decimal Price(Ticket t, DateTime exitTime); }
class HourlyPricing : IPricingStrategy { /* rate per VehicleType, rounded up to the hour */ }

interface ISpotAllocationStrategy { ParkingSpot? FindSpot(IEnumerable<Floor> floors, Vehicle v); }
class NearestFirst : ISpotAllocationStrategy { }

interface IPayment { bool Pay(decimal amount); }   // CardPayment, UpiPayment, CashPayment

class ParkingLot {
    List<Floor> Floors; ISpotAllocationStrategy Allocator; IPricingStrategy Pricing;
    Ticket? Enter(Vehicle v);                        // find a spot, park, issue a ticket
    decimal Exit(Ticket t, IPayment payment);        // price, pay, free the spot
}
```

The flow to say out loud: **Enter**: find a spot, then park, then issue a ticket (or "lot full").
**Exit**: price the ticket, take the payment, mark it paid, free the spot, update the display.

## Step 5: patterns and SOLID (say where, and why)

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | `IPricingStrategy`, `ISpotAllocationStrategy` | Weekend prices or "nearest to the lift" without changing `ParkingLot` |
| **Factory** | creating spots or vehicles from a type | One place knows which class to build |
| **Singleton** | `ParkingLot` (be careful) | One lot per process. Say the downside: hard to test; prefer one instance through DI |
| **Observer** | `DisplayBoard` listens for park and leave events | The board updates without the spot knowing about boards |
| **State** (optional) | `Ticket` Active, Paid, Lost | Only legal moves, like the ride states in CabDemo |

SOLID, one line each, with this design:
- **S**: `ParkingLot` coordinates; pricing lives in `HourlyPricing`, not in the lot.
- **O**: a new price rule is a new `IPricingStrategy` class; existing code doesn't change.
- **L**: any `IPayment` works where `IPayment` is expected.
- **I**: small interfaces (`IPayment` has one method), not one giant `IParkingService`.
- **D**: `ParkingLot` depends on the interfaces, injected through the constructor (like your .NET DI at work).

## Step 6: concurrency and edge cases

- **Two cars at two entrances get the same free spot.** It's the same race as two drivers
  accepting one ride: check-then-act. Fixes: lock per floor or spot (`lock` in one process), or
  in a database `UPDATE Spot SET IsFree = 0 WHERE Id = @id AND IsFree = 1` and check rows
  affected == 1, the same as CabDemo.
- Lot full: `Enter` returns null and the display shows "Full".
- Lost ticket: a flat maximum fee, found by plate number.
- Payment fails: the ticket stays Active and the gate stays closed. Retry, or another method.
- A car parks in the wrong spot size: out of scope, but say that sensors could flag it.

## Step 7: extensions they ask about

- **EV charging spots:** a new `SpotSize` or a `Features` flag, plus a charging fee in a new
  pricing strategy. Nothing else changes, because of Strategy.
- **Reservations:** a `Reservation` with a time window; the allocator skips reserved spots.
- **Many lots in a city:** now it's HLD: a service with a database per lot, and an API for apps.

---

## The 60-second version (say this first, then go deeper when asked)

"I'd start by clarifying the requirements: floors, vehicle types, spot sizes, and how pricing
and payment work. The core classes are ParkingLot, Floor, ParkingSpot, Vehicle and Ticket. A lot
has floors, a floor has spots, and a ticket links a vehicle to a spot with the entry time. On
entry, an allocation strategy finds a spot that fits, and we issue a ticket. On exit, a pricing
strategy works out the fee, we take payment and free the spot. I use Strategy for pricing and
allocation so new rules don't change the core, and dependency injection for testing. The
tricky part is concurrency: two entrances can grab the same spot, so allocation must be atomic,
with a lock or a conditional update that checks rows affected."

## Terms to say naturally

composition, inheritance, interface, enum, Strategy, Factory, Singleton (and why to be careful),
Observer, SOLID, dependency injection, atomic, race condition, extensibility.

## Grill yourself (answer out loud, under 1 minute each)

1. Why is pricing an interface and not a method on `ParkingLot`?
2. Enum or subclasses for vehicles: which, and when would you switch?
3. Two cars, one spot, same moment: what happens in your design?
4. Where would a Singleton hurt you?
5. Add monthly passes: which classes change?
