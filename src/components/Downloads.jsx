import { motion } from "framer-motion";
import { Download, Monitor, Apple, CheckCircle } from "lucide-react";
import { Button } from "./ui/button";

const platforms = [
  {
    name: "Windows",
    icon: Monitor,
    version: "v1.0.0",
    size: "85 MB",
    available: true,
    requirements: [
      "Windows 10 or later",
      "64-bit processor",
      "4GB RAM minimum",
    ],
  },
  {
    name: "macOS",
    icon: Apple,
    version: "v1.0.0",
    size: "92 MB",
    available: true,
    requirements: [
      "macOS 11 (Big Sur) or later",
      "Apple Silicon or Intel",
      "4GB RAM minimum",
    ],
  },
  {
    name: "Linux",
    icon: Monitor,
    version: "v1.0.0",
    size: "78 MB",
    available: true,
    requirements: [
      "Ubuntu 20.04+ or equivalent",
      "64-bit processor",
      "4GB RAM minimum",
    ],
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export const Downloads = () => {
  return (
    <section
      id="download"
      className="relative py-20 sm:py-24 md:py-28 overflow-hidden w-6xl"
    >
      {/* Background */}
      <div className="absolute inset-0 bg-linear-to-b from-background via-primary/5 to-background" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,hsl(var(--primary)/0.1),transparent_60%)]" />

      <div className="relative z-10 px-4 sm:px-6 md:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-10 sm:mb-14 md:mb-16"
        >
          <span className="text-primary font-semibold text-xs sm:text-sm tracking-wider uppercase mb-3 sm:mb-4 block">
            Download
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6">
            Get <span className="gradient-text">ASM Studio</span>
          </h2>
          <p className="text-muted-foreground text-base sm:text-lg max-w-xl sm:max-w-2xl mx-auto">
            Available for all major platforms. Download now and start coding in
            minutes.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6 max-w-5xl mx-auto mb-10 sm:mb-12"
        >
          {platforms.map((platform) => (
            <motion.div
              key={platform.name}
              variants={itemVariants}
              whileHover={{ y: -6 }}
              className="group"
            >
              <div className="glass-card p-5 sm:p-6 h-full flex flex-col items-center text-center transition-all duration-300 hover:border-primary/40">
                <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-linear-to-br from-primary/20 to-accent/20 flex items-center justify-center mb-4 sm:mb-5">
                  <platform.icon className="w-7 h-7 sm:w-8 sm:h-8 text-primary" />
                </div>

                <h3 className="text-lg sm:text-xl font-bold mb-2">
                  {platform.name}
                </h3>

                <div className="flex items-center gap-2 sm:gap-3 text-xs sm:text-sm text-muted-foreground mb-3 sm:mb-4">
                  <span>{platform.version}</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground" />
                  <span>{platform.size}</span>
                </div>

                <Button
                  className="w-full mb-4 bg-primary text-primary-foreground hover:bg-primary/90 hover-glow"
                  disabled={!platform.available}
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </Button>

                {/* Requirements */}
                <div className="mt-auto pt-4 border-t border-border w-full">
                  <p className="text-xs text-muted-foreground mb-2">
                    Requirements:
                  </p>
                  <ul className="space-y-1">
                    {platform.requirements.map((req, i) => (
                      <li
                        key={i}
                        className="text-xs text-muted-foreground/80 flex items-center gap-2"
                      >
                        <CheckCircle className="w-3 h-3 text-primary shrink-0" />
                        <span>{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="text-center mt-6 sm:mt-8 space-y-1 sm:space-y-2"
        >
          <p className="text-xs sm:text-sm text-muted-foreground">
            Current Version:{" "}
            <span className="text-foreground font-medium">1.0.0</span> •
            Released December 2024
          </p>
        </motion.div>
      </div>
    </section>
  );
};
