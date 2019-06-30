#include "actions.hpp"

#include "BLI_hash.h"

namespace BParticles {

class KillAction : public Action {
  void execute(EventExecuteInterface &interface) override
  {
    interface.kill(interface.particles().indices());
  }
};

class MoveAction : public Action {
 private:
  float3 m_offset;

 public:
  MoveAction(float3 offset) : m_offset(offset)
  {
  }

  void execute(EventExecuteInterface &interface) override
  {
    ParticleSet &particles = interface.particles();

    auto positions = particles.attributes().get_float3("Position");
    for (uint pindex : particles.indices()) {
      positions[pindex] += m_offset;
    }
  }
};

class SpawnAction : public Action {
  void execute(EventExecuteInterface &interface) override
  {
    ParticleSet &particles = interface.particles();

    auto positions = particles.attributes().get_float3("Position");

    SmallVector<float3> new_positions;
    SmallVector<float3> new_velocities;
    SmallVector<uint> original_indices;

    for (uint i : particles.range()) {
      uint pindex = particles.get_particle_index(i);
      new_positions.append(positions[pindex] + float3(20, 0, 0));
      new_velocities.append(float3(1, 1, 10));
      original_indices.append(i);
    }

    auto &target = interface.request_emit_target(0, original_indices);
    target.set_float3("Position", new_positions);
    target.set_float3("Velocity", new_velocities);
  }
};

static float random_number()
{
  static uint number = 0;
  number++;
  return BLI_hash_int_01(number) * 2.0f - 1.0f;
}

static float3 random_direction()
{
  return float3(random_number(), random_number(), random_number());
}

class ExplodeAction : public Action {
  void execute(EventExecuteInterface &interface) override
  {
    ParticleSet &particles = interface.particles();

    auto positions = particles.attributes().get_float3("Position");

    SmallVector<float3> new_positions;
    SmallVector<float3> new_velocities;
    SmallVector<uint> original_indices;

    uint parts_amount = 100;
    for (uint i : particles.range()) {
      uint pindex = particles.get_particle_index(i);

      new_positions.append_n_times(positions[pindex], parts_amount);
      original_indices.append_n_times(i, parts_amount);

      for (uint j = 0; j < parts_amount; j++) {
        new_velocities.append(random_direction() * 4);
      }
    }

    auto &target = interface.request_emit_target(1, original_indices);
    target.set_float3("Position", new_positions);
    target.set_float3("Velocity", new_velocities);

    interface.kill(particles.indices());
  }
};

Action *ACTION_kill()
{
  return new KillAction();
}

Action *ACTION_move(float3 offset)
{
  return new MoveAction(offset);
}

Action *ACTION_spawn()
{
  return new SpawnAction();
}

Action *ACTION_explode()
{
  return new ExplodeAction();
}

}  // namespace BParticles
