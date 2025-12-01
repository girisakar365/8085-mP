import { motion } from "framer-motion";
import { BookOpen, Sparkles, Cpu, Zap } from "lucide-react";

const features = [
  {
    icon: BookOpen,
    title: "Jupyter-Style Notebook",
    description:
      "Write, document, and execute code in interactive cells.",
    gradient: "from-primary to-cyan-400",
  },
  {
    icon: Sparkles,
    title: "AI-Powered Assistant",
    description:
      "Get instant help with syntax, debugging, and optimization. Your personal 8085 expert powered by AI.",
    gradient: "from-accent to-pink-400",
  },
  {
    icon: Zap,
    title: "Built-in Assembler",
    description:
      "Compile and assemble your code instantly. Real-time error detection.",
    gradient: "from-yellow-400 to-orange-400",
  },
  {
    icon: Cpu,
    title: "8085 Simulator",
    description:
      "Simulate execution step-by-step. Visualize registers, flags, and memory in real-time.",
    gradient: "from-green-400 to-emerald-400",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 },
  },
};

export const Features = () => {
  return (
    <section
      id="features"
      className="relative py-16 sm:py-24 md:py-32 overflow-hidden"
    >
      {/* Background decoration */}
      <div className="absolute inset-0 bg-linear-to-b from-background via-secondary/20 to-background" />
      <div className="absolute top-1/2 left-0 w-full h-px bg-linear-to-r from-transparent via-primary/20 to-transparent" />

      <div className="container relative z-10 px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12 sm:mb-16"
        >
          <span className="text-primary font-semibold text-sm tracking-wider uppercase mb-4 block">
            Features
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6">
            Everything you need to{" "}
            <span className="gradient-text">master 8085</span>
          </h2>
          <p className="text-muted-foreground text-base sm:text-lg max-w-2xl mx-auto">
            A complete development environment packed with powerful tools for
            learning, writing, and debugging assembly code.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mx-auto"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              variants={itemVariants}
              whileHover={{ y: -8, scale: 1.02 }}
              className="group"
              id={`feature-${index}`}
            >
              <div className="glass-card h-full p-4 sm:p-6 transition-all duration-300 hover:border-primary/30 mt-4 sm:mt-8">
                <div
                  className={`w-10 h-10 sm:w-12 sm:h-12 rounded-[10px] bg-linear-to-br ${feature.gradient} p-0.5 mb-4 sm:mb-5 relative translate-x-1 -translate-y-1`}
                >
                  <div className="w-full h-full bg-card rounded-[10px] flex items-center justify-center absolute top-0 left-0 -translate-x-1 translate-y-1">
                    <feature.icon className="w-5 h-5 sm:w-6 sm:h-6 text-foreground" />
                  </div>
                </div>

                <h3 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 group-hover:text-primary transition-colors">
                  {feature.title}
                </h3>

                <p className="text-muted-foreground text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
