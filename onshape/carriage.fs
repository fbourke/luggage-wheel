FeatureScript 3070;
import(path : "onshape/std/common.fs", version : "3070.0");

/*
 * Luggage spinner carriage — parametric body + reference wheels/axle.
 * Mirrors cad/params.py (WHEEL_SOURCE=ots) from github.com/fbourke/luggage-wheel.
 *
 * Frame: X fore/aft (+X toward the wheels), Y across the case, Z up.
 * Z = 0 is the LAND (recess ceiling the thrust stack bears on); the case skin
 * is at Z = -shaftProtrusion; the floor is at Z = -landToFloor.
 * Retention is OEM-style: the shaft bore closes to a step just below the
 * shaft end and the M5 button head bears on the boss's bottom flat (no washer).
 */

annotation { "Feature Type Name" : "Luggage carriage" }
export const luggageCarriage = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Group Name" : "Envelope", "Collapsed By Default" : false }
        {
            annotation { "Name" : "Wheel diameter" }
            isLength(definition.wheelOD, { (millimeter) : [30, 50, 80] } as LengthBoundSpec);
            annotation { "Name" : "Land to floor" }
            isLength(definition.landToFloor, { (millimeter) : [40, 53.5, 80] } as LengthBoundSpec);
            annotation { "Name" : "Trail (shaft axis to axle axis)" }
            isLength(definition.trail, { (millimeter) : [5, 16, 30] } as LengthBoundSpec);
            annotation { "Name" : "Shaft protrusion (land to shaft end)" }
            isLength(definition.shaftProtrusion, { (millimeter) : [10, 22.92, 40] } as LengthBoundSpec);
        }
        annotation { "Group Name" : "Wheels", "Collapsed By Default" : true }
        {
            annotation { "Name" : "Tread width" }
            isLength(definition.treadW, { (millimeter) : [5, 12, 30] } as LengthBoundSpec);
            annotation { "Name" : "Width over hub bosses" }
            isLength(definition.wheelW, { (millimeter) : [5, 13.7, 30] } as LengthBoundSpec);
            annotation { "Name" : "Hub boss diameter" }
            isLength(definition.bossD, { (millimeter) : [8, 20, 40] } as LengthBoundSpec);
            annotation { "Name" : "Wheel gap (between treads)" }
            isLength(definition.wheelGap, { (millimeter) : [10, 17, 30] } as LengthBoundSpec);
            annotation { "Name" : "Inboard spacer thickness" }
            isLength(definition.inboardT, { (millimeter) : [0, 1, 5] } as LengthBoundSpec);
            annotation { "Name" : "Body to tire clearance" }
            isLength(definition.wheelClear, { (millimeter) : [0.5, 1.5, 5] } as LengthBoundSpec);
            annotation { "Name" : "Show reference wheels and axle" }
            definition.showWheels is boolean;
        }
        annotation { "Group Name" : "Swivel", "Collapsed By Default" : true }
        {
            annotation { "Name" : "Thrust stack height" }
            isLength(definition.thrustH, { (millimeter) : [0, 4, 10] } as LengthBoundSpec);
            annotation { "Name" : "Boss radius" }
            isLength(definition.bossR, { (millimeter) : [8, 13, 25] } as LengthBoundSpec);
            annotation { "Name" : "Boss taper reaches neck at X" }
            isLength(definition.bossTaperX, { (millimeter) : [0, 2, 10] } as LengthBoundSpec);
            annotation { "Name" : "Cap band thickness (full radius under the top face)" }
            isLength(definition.capT, { (millimeter) : [4, 6, 15] } as LengthBoundSpec);
            annotation { "Name" : "Stem radius (below the 45° cone)" }
            isLength(definition.stemR, { (millimeter) : [8, 9.5, 13] } as LengthBoundSpec);
            annotation { "Name" : "Cap / stem edge rounds" }
            isLength(definition.capEdgeR, { (millimeter) : [0, 2, 4] } as LengthBoundSpec);
            annotation { "Name" : "Bushing bore diameter" }
            isLength(definition.bushingBoreD, { (millimeter) : [6, 12, 20] } as LengthBoundSpec);
            annotation { "Name" : "Bushing length" }
            isLength(definition.bushingL, { (millimeter) : [5, 15, 25] } as LengthBoundSpec);
            annotation { "Name" : "Shaft clearance bore diameter" }
            isLength(definition.shaftClearD, { (millimeter) : [6, 10.4, 20] } as LengthBoundSpec);
            annotation { "Name" : "Lift float (flat above the bottomed bolt head)" }
            isLength(definition.liftFloat, { (millimeter) : [0.1, 0.3, 2] } as LengthBoundSpec);
            annotation { "Name" : "Bolt stick-out: shaft end to head underside, bolt bottomed" }
            isLength(definition.boltStickout, { (millimeter) : [2.5, 8.5, 15] } as LengthBoundSpec);
            annotation { "Name" : "Bolt shank hole diameter" }
            isLength(definition.boltHoleD, { (millimeter) : [3, 5.5, 9] } as LengthBoundSpec);
        }
        annotation { "Group Name" : "Arm", "Collapsed By Default" : true }
        {
            annotation { "Name" : "Axle boss radius" }
            isLength(definition.axleBossR, { (millimeter) : [5, 9, 20] } as LengthBoundSpec);
            annotation { "Name" : "Axle bore diameter" }
            isLength(definition.axleD, { (millimeter) : [3, 6, 12] } as LengthBoundSpec);
            annotation { "Name" : "Arm leaves flat at X" }
            isLength(definition.armFrontX, { (millimeter) : [3, 6, 15] } as LengthBoundSpec);
            annotation { "Name" : "Arm leaves boss rear at Z (depth below land)" }
            isLength(definition.armTopDepth, { (millimeter) : [5, 12, 20] } as LengthBoundSpec);
            annotation { "Name" : "Vertical edge fillet" }
            isLength(definition.edgeR, { (millimeter) : [0, 2, 5] } as LengthBoundSpec);
            annotation { "Name" : "Arm internal corner radius" }
            isLength(definition.armInnerR, { (millimeter) : [0, 3, 6] } as LengthBoundSpec);
            annotation { "Name" : "Arm outline round" }
            isLength(definition.armEdgeR, { (millimeter) : [0, 2.5, 5] } as LengthBoundSpec);
            annotation { "Name" : "Top perimeter round" }
            isLength(definition.topEdgeR, { (millimeter) : [0, 1.5, 4] } as LengthBoundSpec);
        }
    }
    {
        // ---- derived ---------------------------------------------------------
        const r = definition.wheelOD / 2;
        const axleZ = -(definition.landToFloor - r);
        const top = -definition.thrustH;                                   // body top face
        const stepZ = -definition.shaftProtrusion - definition.liftFloat;                            // step ceiling, just below the shaft end
        const flat = -definition.shaftProtrusion - definition.boltStickout + definition.liftFloat;   // flat sits liftFloat above the bottomed head
        const armTop = -definition.armTopDepth;
        const neckW = definition.wheelGap - 1 * millimeter;
        const hw = neckW / 2;
        const trail = definition.trail;
        const bossR = definition.bossR;
        const aR = definition.axleBossR;
        const wheelCentreY = hw + definition.inboardT + definition.wheelW / 2;

        if (stepZ >= top - definition.bushingL)
            throw regenError("Shaft too short: bushing would run into the step.");
        if ((definition.shaftClearD - definition.boltHoleD) / 2 < 1.5 * millimeter)
            throw regenError("Bolt hole too large: the step annulus under the shaft end is too narrow.");
        if (armTop <= flat || armTop >= top - 4 * millimeter)
            throw regenError("Arm top must lie between the boss flat and 4 mm below the top face.");

        // ---- neck: side profile on the XZ plane, extruded symmetric in Y ------
        // Three separate sketches + extrudes, then a solid union. (One sketch
        // with all three shapes drops the small circle/rectangle lens because
        // the arm polygon shares edges with the rectangle.)
        const sidePlane = plane(vector(0, 0, 0) * millimeter, vector(0, -1, 0), vector(1, 0, 0)); // sketch (x,y) = world (X,Z)
        var sk = newSketchOnPlane(context, id + "neckSketch", { "sketchPlane" : sidePlane });
        skRectangle(sk, "bossRect", { "firstCorner" : vector(0 * millimeter, flat), "secondCorner" : vector(bossR, top) });
        skSolve(sk);
        const pA = vector(definition.armFrontX, flat);
        const pB = vector(bossR, armTop);
        const c = vector(trail, axleZ);
        const tA = tangentPoint(pA, c, aR, false);   // lower tangent
        const tB = tangentPoint(pB, c, aR, true);    // upper/rear tangent
        var ask = newSketchOnPlane(context, id + "armSketch", { "sketchPlane" : sidePlane });
        skPolyline(ask, "armPoly", { "points" : [pA, tA, c, tB, pB, vector(bossR, flat), pA] });
        skSolve(ask);
        var csk = newSketchOnPlane(context, id + "axleSketch", { "sketchPlane" : sidePlane });
        skCircle(csk, "axleBoss", { "center" : c, "radius" : aR });
        skSolve(csk);
        for (var part in [["neck", "neckSketch"], ["arm", "armSketch"], ["axleBoss", "axleSketch"]])
        {
            opExtrude(context, id + part[0], {
                "entities" : qSketchRegion(id + part[1], true),
                "direction" : vector(0, 1, 0),
                "endBound" : BoundingType.BLIND,
                "endDepth" : hw,
                "startBound" : BoundingType.BLIND,
                "startDepth" : hw
            });
        }

        // ---- swivel boss: plan view on a plane at Z = flat, extruded up to top -
        var bsk = newSketchOnPlane(context, id + "bossSketch", { "sketchPlane" : plane(vector(0 * millimeter, 0 * millimeter, flat), vector(0, 0, 1), vector(1, 0, 0)) });
        // half-round in front (x <= 0) + taper to the neck width
        skArc(bsk, "halfRound", { "start" : vector(0 * millimeter, bossR), "mid" : vector(-bossR, 0 * millimeter), "end" : vector(0 * millimeter, -bossR) });
        skPolyline(bsk, "taper", { "points" : [vector(0 * millimeter, -bossR), vector(definition.bossTaperX, -hw), vector(definition.bossTaperX, hw), vector(0 * millimeter, bossR)] });
        skSolve(bsk);
        opExtrude(context, id + "boss", {
            "entities" : qSketchRegion(id + "bossSketch", true),
            "direction" : vector(0, 0, 1),
            "endBound" : BoundingType.BLIND,
            "endDepth" : top - flat
        });
        // ---- cap: intersect the boss with a body of revolution about the shaft
        //      axis — full radius for the top band, 45° cone, stem around the bore
        const capBandZ = top - definition.capT;
        const stemTopZ = capBandZ - (bossR - definition.stemR);
        if (definition.stemR <= hw + 1 * millimeter)
            throw regenError("Stem radius must exceed half the neck width by 1 mm (grazing intersection).");
        if (definition.stemR - definition.bushingBoreD / 2 < 2.5 * millimeter)
            throw regenError("Stem wall over the bushing bore is under 2.5 mm.");
        var bsk2 = newSketchOnPlane(context, id + "bellSketch", { "sketchPlane" : sidePlane });
        skPolyline(bsk2, "bell", { "points" : [
            vector(0 * millimeter, top + 0.1 * millimeter), vector(bossR + 0.1 * millimeter, top + 0.1 * millimeter),
            vector(bossR + 0.1 * millimeter, capBandZ + 0.1 * millimeter), vector(bossR, capBandZ), vector(definition.stemR, stemTopZ),
            vector(definition.stemR, flat - 0.1 * millimeter), vector(0 * millimeter, flat - 0.1 * millimeter),
            vector(0 * millimeter, top + 0.1 * millimeter)] });
        skSolve(bsk2);
        opRevolve(context, id + "bell", {
            "entities" : qSketchRegion(id + "bellSketch", true),
            "axis" : line(vector(0, 0, 0) * millimeter, vector(0, 0, 1)),
            "angleForward" : 360 * degree
        });
        opBoolean(context, id + "capCut", {
            "tools" : qUnion([qCreatedBy(id + "boss", EntityType.BODY), qCreatedBy(id + "bell", EntityType.BODY)]),
            "operationType" : BooleanOperationType.INTERSECTION
        });
        // the intersection result is a new body; pick it up by exclusion
        //  — only among bodies this feature made, so pre-existing parts in the Part Studio are never touched
        const capBody = qUnion(evaluateQuery(context, qSubtraction(qBodyType(qCreatedBy(id, EntityType.BODY), BodyType.SOLID),
                qUnion([qCreatedBy(id + "neck", EntityType.BODY), qCreatedBy(id + "arm", EntityType.BODY), qCreatedBy(id + "axleBoss", EntityType.BODY)]))));
        if (size(evaluateQuery(context, capBody)) != 1)
            throw regenError("Cap intersection did not produce exactly one body.");
        opBoolean(context, id + "bodyUnion", {
            "tools" : qUnion([qCreatedBy(id + "neck", EntityType.BODY), qCreatedBy(id + "arm", EntityType.BODY),
                              qCreatedBy(id + "axleBoss", EntityType.BODY), capBody]),
            "operationType" : BooleanOperationType.UNION
        });
        const body = qCreatedBy(id + "neck", EntityType.BODY);

        // ---- scoop the boss to the wheel circle where it overhangs the wheels --
        fCylinder(context, id + "scoop", {
            "topCenter" : vector(trail, 2 * bossR + 10 * millimeter, axleZ),
            "bottomCenter" : vector(trail, -(2 * bossR + 10 * millimeter), axleZ),
            "radius" : r + definition.wheelClear
        });
        // but keep the neck: only cut where |y| > hw
        fCuboid(context, id + "neckKeep", {
            "corner1" : vector(-2 * bossR, -hw, axleZ - 2 * r),
            "corner2" : vector(trail + 2 * r, hw, 5 * millimeter)
        });
        opBoolean(context, id + "scoopMinusNeck", {
            "tools" : qCreatedBy(id + "neckKeep", EntityType.BODY),
            "targets" : qCreatedBy(id + "scoop", EntityType.BODY),
            "operationType" : BooleanOperationType.SUBTRACTION
        });
        opBoolean(context, id + "cutScoop", {
            "tools" : qCreatedBy(id + "scoop", EntityType.BODY),
            "targets" : body,
            "operationType" : BooleanOperationType.SUBTRACTION
        });

        // ---- DFM / cosmetics (all best effort; a failed fillet leaves the edge sharp) ----
        // internal corner radii where the arm meets the flat (pA) and the boss rear (pB)
        if (definition.armInnerR > 0)
        {
            const yEdges = qParallelEdges(qOwnedByBody(body, EntityType.EDGE), vector(0, 1, 0));
            filletCascade(context, id + "innerR", qUnion([
                qContainsPoint(yEdges, vector(definition.armFrontX, 0 * millimeter, flat)),
                qContainsPoint(yEdges, vector(bossR, 0 * millimeter, armTop))]), definition.armInnerR);
        }
        // arm outline rounds: edges lying in the neck side planes, outside the boss footprint
        if (definition.armEdgeR > 0)
        {
            var armEdges = [];
            for (var side in [1, -1])
            {
                const sidePlaneQ = qCoincidesWithPlane(qOwnedByBody(body, EntityType.EDGE),
                        plane(vector(0 * millimeter, side * hw, 0 * millimeter), vector(0, 1, 0)));
                for (var e in evaluateQuery(context, sidePlaneQ))
                {
                    const bb = evBox3d(context, { "topology" : e });
                    const cx = (bb.minCorner[0] + bb.maxCorner[0]) / 2;
                    const cz = (bb.minCorner[2] + bb.maxCorner[2]) / 2;
                    if (cx > bossR + 0.2 * millimeter || cz < flat - 0.2 * millimeter)
                        armEdges = append(armEdges, e);
                }
            }
            if (size(armEdges) > 0)
                filletCascade(context, id + "armRound", qUnion(armEdges), definition.armEdgeR);
        }
        // cap underside and cone->stem edges: arcs at those heights in front of the axis
        if (definition.capEdgeR > 0)
        {
            for (var zr in [[capBandZ, "capRound"], [stemTopZ, "stemRound"]])
            {
                var arcs = [];
                const q = qGeometry(qCoincidesWithPlane(qOwnedByBody(body, EntityType.EDGE),
                        plane(vector(0 * millimeter, 0 * millimeter, zr[0]), vector(0, 0, 1))), GeometryType.ARC);
                for (var e in evaluateQuery(context, q))
                {
                    const bb = evBox3d(context, { "topology" : e });
                    if ((bb.minCorner[0] + bb.maxCorner[0]) / 2 < 0 * millimeter)
                        arcs = append(arcs, e);
                }
                if (size(arcs) > 0)
                    filletCascade(context, id + zr[1], qUnion(arcs), definition.capEdgeR);
            }
        }
        // vertical taper / boss corners and stem/neck junctions
        if (definition.edgeR > 0)
        {
            const vert = qParallelEdges(qOwnedByBody(body, EntityType.EDGE), vector(0, 0, 1));
            try silent
            {
                opFillet(context, id + "fillet", { "entities" : vert, "radius" : definition.edgeR });
            }
        }
        // top perimeter round
        if (definition.topEdgeR > 0)
        {
            filletCascade(context, id + "topRound", qCoincidesWithPlane(qOwnedByBody(body, EntityType.EDGE),
                    plane(vector(0 * millimeter, 0 * millimeter, top), vector(0, 0, 1))), definition.topEdgeR);
        }

        // ---- bores -------------------------------------------------------------
        fCylinder(context, id + "bushingBore", {
            "topCenter" : vector(0 * millimeter, 0 * millimeter, top + 1 * millimeter),
            "bottomCenter" : vector(0 * millimeter, 0 * millimeter, top - definition.bushingL),
            "radius" : definition.bushingBoreD / 2
        });
        fCylinder(context, id + "clearBore", {
            "topCenter" : vector(0 * millimeter, 0 * millimeter, top - definition.bushingL + 1 * millimeter),
            "bottomCenter" : vector(0 * millimeter, 0 * millimeter, stepZ),
            "radius" : definition.shaftClearD / 2
        });
        fCylinder(context, id + "boltHole", {
            "topCenter" : vector(0 * millimeter, 0 * millimeter, stepZ + 1 * millimeter),
            "bottomCenter" : vector(0 * millimeter, 0 * millimeter, flat - 1 * millimeter),
            "radius" : definition.boltHoleD / 2
        });
        fCylinder(context, id + "axleBore", {
            "topCenter" : vector(trail, hw + 1 * millimeter, axleZ),
            "bottomCenter" : vector(trail, -hw - 1 * millimeter, axleZ),
            "radius" : definition.axleD / 2
        });
        opBoolean(context, id + "cutBores", {
            "tools" : qUnion([qCreatedBy(id + "bushingBore", EntityType.BODY), qCreatedBy(id + "clearBore", EntityType.BODY), qCreatedBy(id + "boltHole", EntityType.BODY), qCreatedBy(id + "axleBore", EntityType.BODY)]),
            "targets" : body,
            "operationType" : BooleanOperationType.SUBTRACTION
        });
        setProperty(context, { "entities" : body, "propertyType" : PropertyType.NAME, "value" : "Carriage body" });

        // ---- reference wheels + axle (not for manufacture) ---------------------
        if (definition.showWheels)
        {
            const axleL = 2 * (wheelCentreY + definition.wheelW / 2) + 6 * millimeter;
            fCylinder(context, id + "axle", {
                "topCenter" : vector(trail, axleL / 2, axleZ),
                "bottomCenter" : vector(trail, -axleL / 2, axleZ),
                "radius" : definition.axleD / 2 - 0.05 * millimeter
            });
            setProperty(context, { "entities" : qCreatedBy(id + "axle", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "Axle (ref)" });
            for (var side in [1, -1])
            {
                const yc = side * wheelCentreY;
                const wid = id + ("wheel" ~ (side > 0 ? "L" : "R"));
                fCylinder(context, wid + "tread", {
                    "topCenter" : vector(trail, yc + definition.treadW / 2, axleZ),
                    "bottomCenter" : vector(trail, yc - definition.treadW / 2, axleZ),
                    "radius" : r
                });
                fCylinder(context, wid + "boss", {
                    "topCenter" : vector(trail, yc + definition.wheelW / 2, axleZ),
                    "bottomCenter" : vector(trail, yc - definition.wheelW / 2, axleZ),
                    "radius" : definition.bossD / 2
                });
                opBoolean(context, wid + "union", {
                    "tools" : qUnion([qCreatedBy(wid + "tread", EntityType.BODY), qCreatedBy(wid + "boss", EntityType.BODY)]),
                    "operationType" : BooleanOperationType.UNION
                });
                fCylinder(context, wid + "bore", {
                    "topCenter" : vector(trail, yc + definition.wheelW, axleZ),
                    "bottomCenter" : vector(trail, yc - definition.wheelW, axleZ),
                    "radius" : definition.axleD / 2
                });
                opBoolean(context, wid + "cutBore", {
                    "tools" : qCreatedBy(wid + "bore", EntityType.BODY),
                    "targets" : qCreatedBy(wid + "tread", EntityType.BODY),
                    "operationType" : BooleanOperationType.SUBTRACTION
                });
                setProperty(context, { "entities" : qCreatedBy(wid + "tread", EntityType.BODY), "propertyType" : PropertyType.NAME, "value" : "Wheel (ref) " ~ (side > 0 ? "L" : "R") });
            }
        }
    }, {
        wheelOD : 50 * millimeter, landToFloor : 53.5 * millimeter, trail : 16 * millimeter, shaftProtrusion : 22.92 * millimeter,
        treadW : 12 * millimeter, wheelW : 13.7 * millimeter, bossD : 20 * millimeter, wheelGap : 17 * millimeter,
        inboardT : 1 * millimeter, wheelClear : 1.5 * millimeter, showWheels : true,
        thrustH : 4 * millimeter, bossR : 13 * millimeter, bossTaperX : 2 * millimeter, bushingBoreD : 12 * millimeter,
        capT : 6 * millimeter, stemR : 9.5 * millimeter, capEdgeR : 2 * millimeter,
        bushingL : 15 * millimeter, shaftClearD : 10.4 * millimeter, liftFloat : 0.3 * millimeter, boltStickout : 8.5 * millimeter, boltHoleD : 5.5 * millimeter,
        axleBossR : 9 * millimeter, axleD : 6 * millimeter, armFrontX : 6 * millimeter, armTopDepth : 12 * millimeter,
        edgeR : 2 * millimeter, armInnerR : 3 * millimeter, armEdgeR : 2.5 * millimeter, topEdgeR : 1.5 * millimeter
    });

/** Fillet with a shrinking radius; give up silently if no radius works. */
function filletCascade(context is Context, id is Id, edges is Query, r is ValueWithUnits)
{
    try silent { opFillet(context, id + "a", { "entities" : edges, "radius" : r }); return; }
    try silent { opFillet(context, id + "b", { "entities" : edges, "radius" : r * 0.75 }); return; }
    try silent { opFillet(context, id + "c", { "entities" : edges, "radius" : r * 0.5 }); return; }
}

/** Tangent point on the circle (c, r) from an external 2D point p. upper=true picks the candidate with the larger y. */
function tangentPoint(p is Vector, c is Vector, r is ValueWithUnits, upper is boolean) returns Vector
{
    const d = norm(p - c);
    const phi = atan2(p[1] - c[1], p[0] - c[0]);
    const alpha = acos(r / d);
    const a = c + r * vector(cos(phi + alpha), sin(phi + alpha));
    const b = c + r * vector(cos(phi - alpha), sin(phi - alpha));
    if (upper)
        return a[1] > b[1] ? a : b;
    return a[1] < b[1] ? a : b;
}
