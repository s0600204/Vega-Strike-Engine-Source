#ifndef _CMD_FLYBYWIRE_H_
#define _CMD_FLYBYWIRE_H_
#include "order.h"
namespace Orders {
class MatchLinearVelocity : public Order {
 protected:
  Vector desired_velocity;//werld space... generally r*speed;
  bool LocalVelocity;//specified in Local or World coordinates
  bool willfinish;
 public:
  MatchLinearVelocity (const Vector &desired, bool Local, bool fini=true):Order (MOVEMENT|LOCATION), desired_velocity(desired),LocalVelocity(Local),willfinish(fini) {done = false;}
  void Execute ();
  void SetDesiredVelocity (const Vector &desired, bool Local) {desired_velocity=desired;LocalVelocity=Local;}
};
class MatchAngularVelocity : public Order {
 protected:
  Vector desired_ang_velocity;//werld space... generally r*speed;
  bool LocalAng;//specified in Local or World coordinates
  bool willfinish;
 public:
  MatchAngularVelocity (const Vector &desired, bool Local, bool fini=true):Order (FACING|LOCATION), desired_ang_velocity(desired),LocalAng(Local), willfinish(fini) {done = false;}
  void Execute ();
  void SetDesiredAngularVelocity (const Vector &desired, bool Local) {desired_ang_velocity=desired;LocalAng=Local;}
};

class MatchVelocity : public MatchAngularVelocity {
 protected:
  Vector desired_velocity;//werld space... generally r*speed;
  bool LocalVelocity;
 public:
  MatchVelocity (const Vector &desired,const Vector &desired_ang, const bool Local, const bool fini=true) :MatchAngularVelocity (desired_ang,Local,fini),desired_velocity(desired), LocalVelocity(Local) {type = FACING | MOVEMENT|LOCATION;}
  void Execute ();
  void SetDesiredVelocity (const Vector &desired, const bool Local) {desired_velocity=desired;LocalVelocity=Local;}
};
}
class FlyByWire : public Orders::MatchVelocity {
 protected:
  bool sheltonslide;
 public:
  FlyByWire ();
  void SheltonSlide (bool onoff);
  void Stop (float percentage);
  void Right (float percentage);//pass in the percentage of the turn they were turnin right.  -%age indicates left
  void Up (float percentage);//pass in the percentage of the turn they were turning up
  void RollRight (float percentage);
  void Afterburn (float percentage);
  void Accel (float percentage);//negative is decel... 0 = nothing
  void Execute();
};
#endif
