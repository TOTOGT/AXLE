import { useRef, useState, useMemo } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Html, Line, Sphere, Cylinder } from "@react-three/drei";
import * as THREE from "three";

// ─── DATA ──────────────────────────────────────────────────────────────────────
const SPECIMEN = {
  id: "rosa-rugosa",
  commonName: "Rugosa Rose",
  scientificName: "Rosa rugosa",
  family: "Rosaceae",
  genus: "Rosa",
  species: "rugosa",
  authority: "Thunb.",
  nativeRange: "Eastern Asia (Japan, Korea, China)",
  bloomSeason: "May – September",
  profile: [
    "Rosa rugosa is a hardy, deciduous shrub prized for its intensely fragrant, crinkled petals and vivid rose hips.",
    "Native to coastal regions of eastern Asia, it colonises sandy soils and salt-sprayed dunes with ease.",
    "Its hips are among the richest known plant sources of Vitamin C, used for centuries in folk medicine and tea.",
    "The deeply veined, rugose (wrinkled) leaves give this species both its Latin epithet and its signature textured look.",
  ],
  relatedBiota: [
    {
      name: "Bombus terrestris",
      role: "Primary pollinator",
      note: "Buff-tailed bumblebees are the principal pollinator, collecting both nectar and pollen in a single visit.",
      icon: "🐝",
    },
    {
      name: "Papilio machaon",
      role: "Secondary pollinator",
      note: "Old World Swallowtail butterflies are attracted to the open, flat flower architecture.",
      icon: "🦋",
    },
    {
      name: "Phragmidium tuberculatum",
      role: "Parasitic rust fungus",
      note: "A host-specific rust that produces orange pustules on leaves; rarely fatal but common on cultivated roses.",
      icon: "🍄",
    },
    {
      name: "Diplolepis rosae",
      role: "Gall wasp",
      note: "Induces the 'Robin's pincushion' gall, a mossy red structure visible on wild stems in late summer.",
      icon: "🪲",
    },
  ],
  hotspots: [
    {
      id: "petal",
      label: "Petal",
      scientificTerm: "Petalum",
      description:
        "Five broad, notched petals (occasionally semi-double) in shades of deep pink to magenta; exceptionally fragrant due to geraniol and citronellol.",
      position: [0.75, 0.35, 0.5],
    },
    {
      id: "stamen",
      label: "Stamen",
      scientificTerm: "Stamen",
      description:
        "Numerous golden stamens form a dense central cluster (androphore). Each stamen has a filament topped by an anther that releases pollen.",
      position: [0, 0.05, 0.55],
    },
    {
      id: "sepal",
      label: "Sepal",
      scientificTerm: "Sepalum",
      description:
        "Five lanceolate, pinnate-lobed sepals (calyx) remain attached after petal drop and persist around the developing hip.",
      position: [-0.8, -0.4, 0.4],
    },
    {
      id: "receptacle",
      label: "Receptacle",
      scientificTerm: "Receptaculum",
      description:
        "The urn-shaped, fleshy hypanthium that will develop into the bright red rose hip — a multi-seeded pseudofruit rich in vitamin C.",
      position: [0.05, -0.82, 0.3],
    },
    {
      id: "peduncle",
      label: "Peduncle",
      scientificTerm: "Pedunculus",
      description:
        "The stout, bristly flower stalk bearing scattered glandular prickles. In R. rugosa, these are notably dense and sharp.",
      position: [-0.55, -1.2, 0.1],
    },
  ],
};

// ─── 3D FLOWER MODEL ──────────────────────────────────────────────────────────
// Procedural rose built from Three.js geometry — swap `useGLTF` here for a real .glb/.gltf:
// import { useGLTF } from "@react-three/drei";
// const { scene } = useGLTF("/models/rosa-rugosa.glb");
// return <primitive object={scene} />;

function Petal({ angle, radius = 0.72, tilt = 0.18, color = "#D8506A" }) {
  const shape = useMemo(() => {
    const s = new THREE.Shape();
    s.moveTo(0, 0);
    s.bezierCurveTo(0.22, 0.08, 0.38, 0.55, 0, 0.72);
    s.bezierCurveTo(-0.38, 0.55, -0.22, 0.08, 0, 0);
    return s;
  }, []);

  const extrudeSettings = useMemo(
    () => ({
      depth: 0.04,
      bevelEnabled: true,
      bevelThickness: 0.015,
      bevelSize: 0.01,
      bevelSegments: 3,
    }),
    []
  );

  return (
    <group rotation={[tilt, 0, angle]}>
      <mesh castShadow>
        <extrudeGeometry args={[shape, extrudeSettings]} />
        <meshStandardMaterial
          color={color}
          roughness={0.55}
          metalness={0.02}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}

function StamenCluster() {
  const stamens = useMemo(() => {
    const arr = [];
    for (let i = 0; i < 28; i++) {
      const angle = (i / 28) * Math.PI * 2 + Math.random() * 0.2;
      const r = 0.08 + Math.random() * 0.18;
      arr.push({
        x: Math.cos(angle) * r,
        z: Math.sin(angle) * r,
        h: 0.18 + Math.random() * 0.14,
      });
    }
    return arr;
  }, []);
  return (
    <group position={[0, -0.04, 0]}>
      {stamens.map((s, i) => (
        <group key={i} position={[s.x, 0, s.z]}>
          <mesh>
            <cylinderGeometry args={[0.008, 0.008, s.h, 6]} />
            <meshStandardMaterial color="#E8C547" roughness={0.4} />
          </mesh>
          <mesh position={[0, s.h / 2 + 0.015, 0]}>
            <sphereGeometry args={[0.022, 8, 8]} />
            <meshStandardMaterial color="#F0D060" roughness={0.3} metalness={0.1} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function Sepals() {
  return (
    <group position={[0, -0.5, 0]}>
      {[0, 1, 2, 3, 4].map((i) => {
        const angle = (i / 5) * Math.PI * 2;
        return (
          <mesh
            key={i}
            rotation={[0.3, 0, angle]}
            position={[Math.cos(angle) * 0.08, 0, Math.sin(angle) * 0.08]}
          >
            <coneGeometry args={[0.09, 0.42, 5]} />
            <meshStandardMaterial color="#4A7C59" roughness={0.7} side={THREE.DoubleSide} />
          </mesh>
        );
      })}
    </group>
  );
}

function FlowerModel({ onHotspotClick, activeHotspot }) {
  const groupRef = useRef();
  useFrame((_, delta) => {
    if (groupRef.current && !activeHotspot) {
      groupRef.current.rotation.y += delta * 0.25;
    }
  });

  // Outer petals (5, more spread)
  const outerPetals = useMemo(
    () =>
      Array.from({ length: 5 }, (_, i) => ({
        angle: (i / 5) * Math.PI * 2,
        tilt: 0.42,
        color: "#C44062",
      })),
    []
  );
  // Inner petals (5, more upright)
  const innerPetals = useMemo(
    () =>
      Array.from({ length: 5 }, (_, i) => ({
        angle: (i / 5) * Math.PI * 2 + Math.PI / 5,
        tilt: 0.22,
        color: "#D8506A",
      })),
    []
  );

  return (
    <group ref={groupRef} position={[0, 0.3, 0]}>
      {/* Stem */}
      <mesh position={[0, -1.05, 0]}>
        <cylinderGeometry args={[0.045, 0.06, 1.1, 8]} />
        <meshStandardMaterial color="#3A6B45" roughness={0.8} />
      </mesh>

      {/* Receptacle */}
      <mesh position={[0, -0.52, 0]}>
        <sphereGeometry args={[0.14, 12, 12]} />
        <meshStandardMaterial color="#5A8C62" roughness={0.6} />
      </mesh>

      <Sepals />

      {/* Petals */}
      {outerPetals.map((p, i) => (
        <Petal key={`outer-${i}`} {...p} />
      ))}
      {innerPetals.map((p, i) => (
        <Petal key={`inner-${i}`} {...p} />
      ))}

      <StamenCluster />

      {/* Hotspot markers */}
      {SPECIMEN.hotspots.map((hs) => {
        const isActive = activeHotspot?.id === hs.id;
        return (
          <group key={hs.id} position={hs.position}>
            <mesh
              onClick={(e) => {
                e.stopPropagation();
                onHotspotClick(isActive ? null : hs);
              }}
            >
              <sphereGeometry args={[0.065, 12, 12]} />
              <meshStandardMaterial
                color={isActive ? "#B8860B" : "#F5F0E8"}
                emissive={isActive ? "#7A5700" : "#888880"}
                emissiveIntensity={isActive ? 0.6 : 0.3}
                roughness={0.3}
                metalness={0.5}
              />
            </mesh>
            {/* Leader line rendered via Html to avoid Three.js line complexity */}
            <Html
              center
              distanceFactor={5}
              style={{ pointerEvents: "none", userSelect: "none" }}
            >
              <div
                style={{
                  background: isActive
                    ? "rgba(184,134,11,0.92)"
                    : "rgba(30,24,18,0.78)",
                  color: "#F9F5EC",
                  fontSize: "11px",
                  fontFamily: "'Crimson Text', Georgia, serif",
                  fontStyle: "italic",
                  padding: "3px 8px",
                  borderRadius: "3px",
                  whiteSpace: "nowrap",
                  letterSpacing: "0.03em",
                  border: isActive ? "1px solid #D4A820" : "1px solid rgba(255,255,255,0.15)",
                  cursor: "pointer",
                  pointerEvents: "auto",
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onHotspotClick(isActive ? null : hs);
                }}
              >
                {hs.label}
              </div>
            </Html>
          </group>
        );
      })}
    </group>
  );
}

// ─── UI COMPONENTS ────────────────────────────────────────────────────────────
function TaxonomyRow({ label, value, italic = false }) {
  return (
    <div className="flex justify-between items-baseline py-2 border-b border-stone-200 last:border-0">
      <span className="text-xs uppercase tracking-widest text-stone-400 font-medium">{label}</span>
      <span
        className={`text-sm text-stone-700 ${italic ? "italic" : ""}`}
        style={{ fontFamily: italic ? "'Crimson Text', Georgia, serif" : undefined }}
      >
        {value}
      </span>
    </div>
  );
}

function HotspotPanel({ hotspot, onClose }) {
  if (!hotspot) return null;
  return (
    <div className="mt-4 p-4 rounded-lg border border-amber-200 bg-amber-50/70">
      <div className="flex justify-between items-start mb-1">
        <div>
          <h3 className="text-sm font-semibold text-stone-700 uppercase tracking-wider">
            {hotspot.label}
          </h3>
          <p
            className="text-xs italic text-amber-700 mt-0.5"
            style={{ fontFamily: "'Crimson Text', Georgia, serif" }}
          >
            {hotspot.scientificTerm}
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-stone-400 hover:text-stone-600 text-lg leading-none"
        >
          ×
        </button>
      </div>
      <p className="text-xs text-stone-600 leading-relaxed mt-2">{hotspot.description}</p>
    </div>
  );
}

// ─── MAIN COMPONENT ───────────────────────────────────────────────────────────
export default function DigitalHerbarium() {
  const [activeHotspot, setActiveHotspot] = useState(null);
  const [tab, setTab] = useState("taxonomy"); // taxonomy | facts | biota

  return (
    <div
      className="min-h-screen flex flex-col lg:flex-row"
      style={{ background: "#F7F4EE", fontFamily: "'Crimson Text', Georgia, serif" }}
    >
      {/* ── VIEWER PANE ── */}
      <div className="flex-1 relative" style={{ minHeight: "60vh" }}>
        {/* Header badge */}
        <div className="absolute top-5 left-5 z-10">
          <p
            className="text-xs uppercase tracking-[0.2em] text-stone-400"
            style={{ fontFamily: "system-ui, sans-serif" }}
          >
            Digital Herbarium — Specimen No. 0042
          </p>
          <h1
            className="text-3xl font-normal text-stone-800 leading-tight mt-0.5"
          >
            <em>{SPECIMEN.scientificName}</em>
          </h1>
          <p className="text-sm text-stone-500">{SPECIMEN.authority} · {SPECIMEN.commonName}</p>
        </div>

        {/* Instruction */}
        <div
          className="absolute bottom-5 left-1/2 z-10 text-center"
          style={{ transform: "translateX(-50%)" }}
        >
          <p
            className="text-xs text-stone-400"
            style={{ fontFamily: "system-ui, sans-serif", letterSpacing: "0.05em" }}
          >
            Drag to rotate · Scroll to zoom · Click labels to inspect
          </p>
        </div>

        {/* Canvas */}
        <Canvas
          shadows
          camera={{ position: [0, 0.5, 3.8], fov: 38 }}
          style={{ background: "transparent" }}
          gl={{ antialias: true, alpha: true }}
        >
          <ambientLight intensity={0.55} color="#FFF8F0" />
          <directionalLight
            position={[4, 6, 4]}
            intensity={1.4}
            castShadow
            color="#FFFAF2"
            shadow-mapSize={[1024, 1024]}
          />
          <directionalLight position={[-3, 2, -2]} intensity={0.35} color="#E0E8FF" />
          <pointLight position={[0, 2, 1.5]} intensity={0.3} color="#FFE4B5" />

          <FlowerModel
            onHotspotClick={setActiveHotspot}
            activeHotspot={activeHotspot}
          />

          <OrbitControls
            enablePan={true}
            enableZoom={true}
            minDistance={1.5}
            maxDistance={7}
            minPolarAngle={Math.PI * 0.1}
            maxPolarAngle={Math.PI * 0.85}
            dampingFactor={0.08}
            enableDamping
          />
        </Canvas>
      </div>

      {/* ── SIDEBAR ── */}
      <div
        className="w-full lg:w-96 flex flex-col border-l border-stone-200"
        style={{ background: "#FDFAF5", minHeight: "40vh" }}
      >
        <div className="flex-1 overflow-y-auto p-6">
          {/* Species header */}
          <div className="mb-6 pb-5 border-b border-stone-200">
            <div className="flex items-center gap-2 mb-1">
              <span
                className="text-xs uppercase tracking-widest text-stone-400"
                style={{ fontFamily: "system-ui, sans-serif" }}
              >
                Family
              </span>
              <span className="text-sm italic text-stone-600">{SPECIMEN.family}</span>
            </div>
            <div
              className="text-xs text-stone-400 mt-2"
              style={{ fontFamily: "system-ui, sans-serif", letterSpacing: "0.05em" }}
            >
              {SPECIMEN.nativeRange} · Blooms {SPECIMEN.bloomSeason}
            </div>
          </div>

          {/* Tabs */}
          <div
            className="flex gap-0 mb-5 border border-stone-200 rounded overflow-hidden"
            style={{ fontFamily: "system-ui, sans-serif" }}
          >
            {[
              { id: "taxonomy", label: "Taxonomy" },
              { id: "facts", label: "Profile" },
              { id: "biota", label: "Related Biota" },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`flex-1 py-2 text-xs uppercase tracking-wider transition-colors ${
                  tab === t.id
                    ? "bg-stone-800 text-amber-100"
                    : "bg-transparent text-stone-500 hover:bg-stone-100"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          {tab === "taxonomy" && (
            <div>
              <TaxonomyRow label="Kingdom" value="Plantae" />
              <TaxonomyRow label="Order" value="Rosales" />
              <TaxonomyRow label="Family" value="Rosaceae" italic />
              <TaxonomyRow label="Genus" value="Rosa" italic />
              <TaxonomyRow label="Species" value="R. rugosa" italic />
              <TaxonomyRow label="Authority" value="Thunb. 1784" />
              <TaxonomyRow label="Common name" value="Rugosa Rose" />
              <TaxonomyRow label="Native range" value="E. Asia" />
            </div>
          )}

          {tab === "facts" && (
            <div className="space-y-3">
              {SPECIMEN.profile.map((para, i) => (
                <p key={i} className="text-sm text-stone-600 leading-relaxed">
                  {para}
                </p>
              ))}
            </div>
          )}

          {tab === "biota" && (
            <div className="space-y-3">
              {SPECIMEN.relatedBiota.map((b) => (
                <div key={b.name} className="p-3 rounded-lg border border-stone-200 bg-stone-50/50">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-base">{b.icon}</span>
                    <div>
                      <p className="text-sm italic text-stone-700">{b.name}</p>
                      <p
                        className="text-xs text-stone-400 uppercase tracking-wider"
                        style={{ fontFamily: "system-ui, sans-serif" }}
                      >
                        {b.role}
                      </p>
                    </div>
                  </div>
                  <p className="text-xs text-stone-500 leading-relaxed mt-1">{b.note}</p>
                </div>
              ))}
            </div>
          )}

          {/* Active hotspot panel */}
          <HotspotPanel
            hotspot={activeHotspot}
            onClose={() => setActiveHotspot(null)}
          />
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-stone-200">
          <p
            className="text-xs text-stone-300 text-center"
            style={{ fontFamily: "system-ui, sans-serif", letterSpacing: "0.04em" }}
          >
            G6 LLC · Digital Herbarium Series · {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </div>
  );
}
