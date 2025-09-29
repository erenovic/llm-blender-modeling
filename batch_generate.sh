#!/usr/bin/env bash
set -euo pipefail

# Calls ./generate.sh "<PROMPT>" "<OBJ_NAME>" for each asset below.

# NOTE: Prompts aim for realistic, high-poly meshes with plausible scale and PBR-ready materials.
# Dimensions are in meters. You can instance or duplicate in Blender for counts (e.g., 6 chairs).

NAMES=(
  "dining_table"
  "dining_chair"
  "sideboard_cabinet"
  "dining_rug"
  "crystal_chandelier"
  "wall_sconce_pair"
  "velvet_curtains"
  "framed_painting"
  "floor_plant"
  "table_runner"
  "dinnerware_set"
  "cutlery_set"
  "wine_glass"
  "centerpiece_vase_with_flowers"
  "napkin_ring_set"
)

PROMPTS=(
'Write Blender Python to create a large rectangular dining table sized 2.2 x 1.0 x 0.76 meters, built from solid quarter-sawn oak with a natural matte oil finish. Include slightly beveled edges, breadboard ends, and robust trestle-style legs with a center stretcher. Model realistic many-polygon wood grain with UV-unwrapped planks, subtle end-grain variation, and micro normal detail. Use PBR materials (albedo, roughness, normal), rounded-bevels on edges (0.8–1.5 mm), and keep real-world scale and origin at floor contact.'

'Write Blender Python to create a high-end dining chair with a steam-bent walnut frame, tapered legs, and an ergonomically curved backrest. Seat height 0.45 m, overall height 0.9 m. Add dense beige linen upholstery on seat and inside back with visible fabric weave and stitched seams; outside back remains wood. Include felt glides on feet, 0.3 cm edge bevels, UV-unwrapped wood and fabric, and realistic many-polygon geometry with PBR materials and anisotropic wood grain.'

'Write Blender Python to create a sideboard cabinet 1.8 x 0.45 x 0.9 meters in dark-stained oak with three framed doors and two central drawers. Add inset paneling, soft chamfers, adjustable interior shelves, and solid brass hardware (pulls and soft-close hinges). Model many-polygon details: beveled top, plinth base, hinge knuckles, screw heads. Use PBR materials for wood and aged brass, with slight edge wear and roughness variation.'

'Write Blender Python to create a large woven Persian-style rug sized 3.0 x 2.0 meters with muted red, navy, and cream palette. Include realistic pile height variation, detailed border and medallion pattern via high-resolution UVs, slightly irregular edges, and subtle curl at corners. Use a fiber material with microfibers (normal map), color variation, and soft subsurface scatter-like effect for pile depth. Keep thickness ~8 mm.'

'Write Blender Python to create a crystal chandelier of 0.9 m diameter and 0.8 m drop, bronze-finished frame with eight curved arms, candle-style E12 bulbs, and multiple tiers of cut-glass pendants and chains. Model many-polygon crystal facets, bobeches, and sockets. Use glass with correct IOR ~1.52, thin-walled where suitable, and a brushed bronze PBR metal. Include ceiling canopy, chain links, and a central finial.'

'Write Blender Python to create a pair of wall sconces (instanceable) with antique brass backplate, short curved arm, and frosted cylindrical glass shade (wall clearance ~0.18 m, height 0.28 m). Model screws, set-screw collar, and socket cup. Use frosted glass (roughness ~0.35) and aged brass PBR, with subtle fingerprints and smudges on glass normals. Output two matching assets as a single grouped object.'

'Write Blender Python to create floor-to-ceiling velvet curtains for a 2.2 m wide window, finished length 2.8 m. Deep burgundy velvet with heavy pleats, double fullness, and a gold rope tieback at 1.0 m from floor. Include a matte black curtain rod with finials and ring clips. Model dense cloth folds (many-polygon), thickness, hem, header tape hints, and believable subsurface shading with micro-fiber normals.'

'Write Blender Python to create a large framed painting 1.2 x 0.8 meters with an ornate gilded frame (carved leaf motif) and a classical oil landscape (impasto-style brushstrokes). Model frame profiles with many polygons, miters, and backing board hint. Use PBR gilded metal/leaf with subtle edge wear and micro-scratches; canvas has normal and height variation for brush texture. Include hanging hardware ring at back.'

'Write Blender Python to create a tall floor plant (fiddle-leaf fig) in a ceramic pot: overall height 1.6 m. Model a realistic branching trunk with bark detail, large broad leaves with visible veins, slight curl, translucency, and varied roughness. Pot is 0.35 m diameter, off-white crackle glaze with subtle imperfections. Add topsoil/pebbles surface. Keep many-polygon leaves with individual UVs and varied hue/saturation.'

'Write Blender Python to create a linen table runner 0.35 x 2.0 meters draped centered along the dining table. Off-white stonewashed linen with hemmed edges, slight fraying, and natural wrinkles. Simulate believable cloth drape over table edges. PBR fabric with visible weave normal, roughness variation from use, and thickness. Ensure collision-conforming geometry and UVs aligned to weave direction.'

'Write Blender Python to create a coordinated dinnerware set for one place setting: 32 cm charger plate (brushed brass rim), 28 cm dinner plate (white porcelain with subtle gloss), 22 cm salad plate, and 18 cm bowl (thin lip). Include underside foot rings, slight thickness variations, and proper stacking clearances. Use PBR ceramic with micro-scratches and smudges, and a separate metallic material for the charger rim.'

'Write Blender Python to create a fine cutlery set (fork, knife, spoon) in polished 18/10 stainless steel, each ~21 cm length with balanced curvature and tapered handle. Model thin knife edge, fork tines chamfer, spoon bowl depth, and stamped maker mark. Use metal shader with clearcoat-like sheen, micro-scratches normal map, and subtle fingerprints roughness variation. Provide as three separate objects grouped.'

'Write Blender Python to create a crystal red wine glass: total height 0.23 m, bowl diameter 0.09 m, thin lip ~1.2 mm, long slender stem, and flat foot 0.07 m diameter. Use physically correct glass (IOR ~1.5), thin-walled where appropriate, and ensure smooth normals with slight thickness at transitions. Include a second duplicate scaled for white wine (0.21 m height) as a separate object in the same group.'

'Write Blender Python to create a centerpiece vase with a hand-blown glass body (smoky translucent gray) 0.28 m tall, 0.16 m diameter, with subtle waviness and tiny bubbles. Fill with a mixed floral arrangement: white hydrangea heads, eucalyptus stems, and a few pale pink roses. Model stems, leaves, and petals with many-polygon detail and realistic translucency; water volume inside with correct IOR and meniscus.'

'Write Blender Python to create a set of four brass napkin rings (outer diameter 4.5 cm, width 2.5 cm) with a knurled outer band and smooth inner surface, bundled with linen napkins (0.45 x 0.45 m) in muted sage. Model fabric folds and thickness, seam hems, and ring chamfers. Use PBR aged brass with micro-scratches and fabric with visible weave and slight roughness anisotropy. Provide rings and napkins as grouped objects.'
)

if ((${#NAMES[@]} != ${#PROMPTS[@]})); then
  echo "Error: NAMES and PROMPTS counts differ (${#NAMES[@]} vs ${#PROMPTS[@]})." >&2
  exit 1
fi

echo "Starting batch dining room asset generation..."
for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  prompt="${PROMPTS[$i]}"
  echo ""
  echo ">>> Generating: ${name}"
  ./generate.sh "$prompt" "$name"
done

echo ""
echo "All assets submitted."
