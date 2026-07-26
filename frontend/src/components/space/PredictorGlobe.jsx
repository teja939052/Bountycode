import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { motion } from "framer-motion";

function MatrixGlobe({ probability = 50, color = "#4CC9F0" }) {
  const globe = useRef();
  const wireframe = useRef();
  const nodes = useRef();

  const nodePositions = useMemo(() => {
    const count = 60;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(-1 + (2 * i) / count);
      const theta = Math.sqrt(count * Math.PI) * phi;
      positions[i * 3] = 2.2 * Math.cos(theta) * Math.sin(phi);
      positions[i * 3 + 1] = 2.2 * Math.sin(theta) * Math.sin(phi);
      positions[i * 3 + 2] = 2.2 * Math.cos(phi);
    }
    return positions;
  }, []);

  const probColor = useMemo(() => {
    if (probability >= 70) return new THREE.Color("#4BB543");
    if (probability >= 50) return new THREE.Color("#4CC9F0");
    if (probability >= 30) return new THREE.Color("#F59E0B");
    return new THREE.Color("#EF4444");
  }, [probability]);

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    if (globe.current) {
      globe.current.rotation.y = t * 0.15;
      globe.current.rotation.x = Math.sin(t * 0.1) * 0.1;
    }
    if (wireframe.current) {
      wireframe.current.rotation.y = t * 0.1;
      wireframe.current.rotation.z = t * 0.05;
    }
    if (nodes.current) {
      nodes.current.rotation.y = t * 0.2;
    }
  });

  return (
    <>
      <ambientLight intensity={0.2} />
      <pointLight position={[5, 5, 5]} color={color} intensity={0.8} />
      <pointLight position={[-5, -3, 3]} color="#7209B7" intensity={0.3} />

      {/* Inner glow sphere */}
      <mesh ref={globe}>
        <sphereGeometry args={[1.8, 32, 32]} />
        <meshStandardMaterial
          color={probColor}
          transparent
          opacity={0.08}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Wireframe globe */}
      <mesh ref={wireframe}>
        <sphereGeometry args={[2, 16, 12]} />
        <meshBasicMaterial
          color={color}
          wireframe
          transparent
          opacity={0.15}
        />
      </mesh>

      {/* Drifting nodes */}
      <points ref={nodes}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={nodePositions}
            count={60}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.08}
          color={color}
          transparent
          opacity={0.8}
          blending={THREE.AdditiveBlending}
        />
      </points>
    </>
  );
}

export default function PredictorGlobe({ probability = 50, company = "Company" }) {
  const probColor =
    probability >= 70
      ? "text-cyber-green glow-green"
      : probability >= 50
      ? "text-cyber-blue glow-blue"
      : probability >= 30
      ? "text-cyber-amber"
      : "text-cyber-red";

  return (
    <div className="relative w-full max-w-xl mx-auto p-6 rounded-2xl bg-space-void/60 border border-cyber-blue/20 backdrop-blur-xl shadow-cyber-blue overflow-hidden">
      {/* Background grid */}
      <div className="absolute inset-0 ambient-grid opacity-20 pointer-events-none" />

      {/* Header */}
      <div className="relative z-10 flex justify-between items-center mb-4 border-b border-cyber-blue/20 pb-4">
        <div>
          <span className="text-[10px] font-mono text-cyber-blue/70 tracking-widest uppercase">
            Target Telemetry //
          </span>
          <h2 className="text-2xl font-display font-black text-white tracking-tight mt-0.5">
            {company} Context
          </h2>
        </div>
        <div className="px-3 py-1 rounded-full border border-cyber-purple/40 bg-cyber-purple/10 text-purple-300 text-[10px] font-mono uppercase tracking-wider">
          System Active
        </div>
      </div>

      {/* 3D Globe */}
      <div className="relative h-56 my-4">
        <Canvas camera={{ position: [0, 0, 5.5], fov: 45 }} dpr={[1, 1.5]}>
          <MatrixGlobe probability={probability} />
        </Canvas>

        {/* Score overlay */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, type: "spring" }}
            className="text-center"
          >
            <div className={`text-5xl font-display font-black tracking-tighter ${probColor}`}>
              {Math.round(probability)}%
            </div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-gray-400 mt-1">
              Offer Probability
            </div>
          </motion.div>
        </div>
      </div>

      {/* Directive */}
      <div className="relative z-10 bg-cyber-blue/5 border border-cyber-blue/15 rounded-xl p-4 font-mono text-xs text-gray-300">
        <div className="flex items-center text-cyber-blue font-bold mb-2">
          <span className="status-processing mr-2" />
          SYSTEM DIAGNOSTIC DIRECTIVE:
        </div>
        {probability < 50 ? (
          <p>
            Minimum threshold matrix failing for {company}. Boost your core mechanics
            immediately to stabilize orbit variables.
          </p>
        ) : (
          <p>
            Stable entry trajectory confirmed. Maintain current practice rhythms to
            guarantee operational clearance.
          </p>
        )}
      </div>
    </div>
  );
}
