import { motion } from "framer-motion";

export const DemoPreview = () => {
  return (
    <section id="demo" className="relative py-16 sm:py-24 md:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,hsl(var(--primary)/0.08),transparent_70%)]" />

      <div className="container relative z-10 px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8 sm:mb-12"
        >
          <span className="text-primary font-semibold text-sm tracking-wider uppercase mb-4 block">
            See it in Action
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6">
            Experience the{" "}
            <span className="gradient-text">future of assembly</span>
          </h2>
          <p className="text-muted-foreground text-base sm:text-lg max-w-2xl mx-auto">
            Watch how ASM Studio transforms your coding workflow with
            intelligent features and a beautiful interface.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-5xl mx-auto"
        >
          {/* Demo window frame */}
          <div className="glass-card p-1.5 glow-primary">
            <div className="bg-card rounded-xl overflow-hidden">
              <img src="https://placehold.co/1200x800" alt="logo" className="w-full h-auto" />
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
